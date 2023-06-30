import validators
from ..models import Link
from ..extensions import db
from datetime import datetime
from flask_caching import Cache
from flask_limiter import Limiter
from sqlalchemy.exc import IntegrityError
from flask_limiter.util import get_remote_address
from flask_login import login_required, current_user
from ..utils.views import fresh_login_required, generate_qr_code
from flask import Blueprint, render_template, url_for, request, redirect, abort, send_file

links = Blueprint('links', __name__)

# Create the limiter and cache objects
limiter = Limiter(get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})


@links.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@links.route('/<short_url>')
@cache.cached(timeout=60) # Cache the response for 60 seconds
def redirect_to_url(short_url):
    # Check if the short URL matches a custom URL
    link = Link.query.filter_by(custom_url=short_url).first()
    if not link:
        # If it doesn't, check if it matches a short URL
        link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.visits += 1
    db.session.commit()

    return redirect(link.original_url)


@links.route('/add_link', methods=['POST'])
@limiter.limit("10/minutes") # Limit to 10 requests per minute
@login_required
@fresh_login_required # Require a fresh login to add a link
def add_link():
    # Get the url and custom url from the form
    original_url = request.form['long-url']
    custom_url = request.form['custom-url']

    # Add a default scheme if the URL doesn't have one {turns www.google.com to https://www.google.com}
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url

    # validate the long url
    if not validators.url(original_url):
        return render_template('index.html', invalid=True)

    # check if the custom url is already in use in the database
    if custom_url:
        existing_link = Link.query.filter_by(custom_url=custom_url, user_id=current_user.id).first()
        # if it is found in the database, return the custom url
        if existing_link:
            return render_template('link_added.html', custom_url_exists=True, new_link=existing_link.custom_url, original_url=existing_link.original_url, visits=existing_link.visits, custom_url=existing_link.custom_url)
        # if it isn't found in the database, add it to the Link object
        else:
            link = Link(original_url=original_url, custom_url=custom_url, user=current_user)
            try:
                link.save()
            except IntegrityError:
                db.session.rollback()
                return render_template('errors/500.html')
            return render_template('link_added.html', new_link=link.custom_url, original_url=link.original_url, custom_url=link.custom_url)
        
    # check if the original_url is already in the database and does not have a custom url
    short_link = Link.query.filter_by(original_url=original_url, custom_url=None, user=current_user).first()

    # if it is, return the existing short url
    if short_link:
        return render_template('link_added.html', new_link=short_link.short_url, original_url=short_link.original_url, visits=short_link.visits, short_url=short_link.short_url, custom_url=short_link.custom_url)
    
    # if it isn't, create a new Link object, save it, and return the new short url
    else:
        link = Link(original_url=original_url, user=current_user)
        link.save()

        return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url)


@links.route('/qr_code/<short_url>')
def generate_qr_code_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        img_io = generate_qr_code(link.original_url)
        return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    else:
        custom_link = Link.query.filter_by(custom_url=short_url).first()
        if custom_link:
            img_io = generate_qr_code(custom_link.original_url)
            return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    return 'URL not found.'

@links.route('/stats')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def stats():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=request.url))
    links = Link.query.filter_by(user=current_user).all()
    
    return render_template('stats.html', links=links)


@links.route('/link/<int:link_id>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_link(link_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=request.url))
    link = Link.query.get_or_404(link_id)
    if link.user_id != current_user.id:
        abort(403)

    # check if the link is a custom url or a short url
    if link.custom_url:
        return redirect(url_for('links.view_custom_link', custom_url=link.custom_url))
    else:
        return redirect(url_for('links.view_short_link', short_url=link.short_url))
    

@links.route('/link/custom/<custom_url>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_custom_link(custom_url):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=request.url))
    link = Link.query.filter_by(custom_url=custom_url).first_or_404()
    if link.user_id != current_user.id:
        abort(403)
    return render_template('link_details.html', link=link, new_link=link.custom_url, custom_url=link.custom_url)


@links.route('/link/short/<short_url>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_short_link(short_url):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=request.url))
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    if link.user_id != current_user.id:
        abort(403)
    return render_template('link_details.html', link=link, new_link=link.short_url)


@links.route('/download/<qr_code_url>')
@login_required
@fresh_login_required
def download_qr_code(qr_code_url):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', next=request.url))
    # Build the path to the QR code file
    link = Link.query.filter_by(short_url=qr_code_url).first() or Link.query.filter_by(custom_url=qr_code_url).first()
    if link:
        img_io = generate_qr_code(link.short_url if link.short_url else link.custom_url)
        filename=f'qr_code_{link.short_url if link.short_url else link.custom_url}.png'
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=filename)
    return 'URL not found.'


@links.route('/delete-url/<int:url_id>', methods=['POST'])
@login_required
def delete_url(url_id):
    url = Link.query.get_or_404(url_id)

    # Check if the current user is the owner of the URL
    if url.user_id != current_user.id:
        abort(403)

    db.session.delete(url)
    db.session.commit()
    
    return redirect(url_for('main.index'))
