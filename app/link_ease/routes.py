import validators, os
from datetime import datetime
from .models import Link, User
from flask_caching import Cache
from flask_limiter import Limiter
from .extensions import db, bcrypt
from flask_limiter.util import get_remote_address
from .utils.views import fresh_login_required, generate_qr_code
from flask_login import login_required, current_user, login_user, logout_user
from flask import Blueprint, render_template, url_for, request, redirect, flash, abort, send_file, current_app

# Create the limiter and cache objects
limiter = Limiter(get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

short = Blueprint('short', __name__)

@short.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@short.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@short.app_errorhandler(403)
def error_404(error):
    return render_template('403.html'), 403

@short.route('/<short_url>')
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

@short.route('/')
def index():
    return render_template('index.html')

@short.route('/add_link', methods=['POST'])
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
            return render_template('link_added.html', custom_url_exists=True, new_link=existing_link.custom_url, original_url=existing_link.original_url, qr_code_url=existing_link.qr_code_url, visits=existing_link.visits)
        # if it isn't found in the database, add it to the Link object
        else:
            link = Link(original_url=original_url, custom_url=custom_url, user=current_user)
            link.qr_code_url = generate_qr_code(link.original_url, custom_url)  # Generate QR code for the short URL and save it with the custom url
            link.save()
            return render_template('link_added.html', new_link=link.custom_url, original_url=link.original_url, qr_code_url=link.qr_code_url)
        
    # check if the original_url is already in the database and does not have a custom url
    short_link = Link.query.filter_by(original_url=original_url, custom_url=None, user=current_user).first()

    # if it is, return the existing short url
    if short_link:
        return render_template('link_added.html', new_link=short_link.short_url, original_url=short_link.original_url, qr_code_url=short_link.qr_code_url, visits=short_link.visits)
    
    # if it isn't, create a new Link object, save it, and return the new short url
    else:
        link = Link(original_url=original_url, user=current_user)
        link.qr_code_url = generate_qr_code(link.original_url, link.short_url)  # Generate QR code for the short URL and save it with the short url
        link.save()
        return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url, qr_code_url=link.qr_code_url)




@short.route('/stats')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def stats():
    if not current_user.is_authenticated:
        return redirect(url_for('short.login', next=request.url))
    links = Link.query.filter_by(user=current_user).all()
    
    return render_template('stats.html', links=links)


@short.route('/link/<int:link_id>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_link(link_id):
    if not current_user.is_authenticated:
        return redirect(url_for('short.login', next=request.url))
    link = Link.query.get_or_404(link_id)
    if link.user_id != current_user.id:
        abort(403)

    # check if the link is a custom url or a short url
    if link.custom_url:
        return redirect(url_for('short.view_custom_link', custom_url=link.custom_url))
    else:
        return redirect(url_for('short.view_short_link', short_url=link.short_url))
    

@short.route('/link/custom/<custom_url>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_custom_link(custom_url):
    if not current_user.is_authenticated:
        return redirect(url_for('short.login', next=request.url))
    link = Link.query.filter_by(custom_url=custom_url).first_or_404()
    if link.user_id != current_user.id:
        abort(403)
    return render_template('link_details.html', link=link, new_link=link.custom_url, qr_code_url=link.qr_code_url)


@short.route('/link/short/<short_url>')
@cache.cached(timeout=10)  # Cache the response for 10 seconds
@login_required
@fresh_login_required
def view_short_link(short_url):
    if not current_user.is_authenticated:
        return redirect(url_for('short.login', next=request.url))
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    if link.user_id != current_user.id:
        abort(403)
    return render_template('link_details.html', link=link, new_link=link.short_url, qr_code_url=link.qr_code_url)


@short.route('/download/<qr_code_url>')
@login_required
@fresh_login_required
def download_qr_code(qr_code_url):
    if not current_user.is_authenticated:
        return redirect(url_for('short.login', next=request.url))
    # Build the path to the QR code file
    qr_code_path = os.path.join(current_app.root_path, 'static', 'image', qr_code_url)

    # Check if the file exists
    if os.path.exists(qr_code_path):
        return send_file(qr_code_path, mimetype='image/png', as_attachment=True)
    else:
        abort(404)


@short.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('short.index'))
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm password match
        if password != confirm_password:
            # flash a message to the user
            flash('Passwords do not match', 'danger')
            return render_template('register.html', password_match=False, error_message='Passwords do not match')
        
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # flash a message to the user
            flash('Email already exists', 'danger')
            return render_template('register.html', email_exists=True, error_message='Email already in use')
        # create a new user object and hash the password
        user = User(username=username, email=email)
        user.set_password(password)
        # save the user object
        user.save()
        # send a message to the user
        flash('You have successfully registered! Please log in.','success')
        return redirect(url_for('short.login'))

    return render_template('register.html')


@short.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('short.index'))
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember_me', False) # it uses get method with a default value


        # Check if the email exists and passwords match with the database
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Log the user in
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('short.index'))
        else:
            # flash a message to the user
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html')


@short.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('short.index'))
