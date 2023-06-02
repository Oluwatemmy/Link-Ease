from flask import Blueprint, render_template, url_for, request, redirect
from .models import Link
from .extensions import db
import validators
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create the limiter and cache objects
limiter = Limiter(key_func=get_remote_address)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

short = Blueprint('short', __name__)


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
        existing_link = Link.query.filter_by(custom_url=custom_url).first()
        # if it is found in the database, return the custom url
        if existing_link:
            return render_template('link_added.html', custom_url_exists=True, new_link=existing_link.custom_url, original_url=existing_link.original_url)
        # if it isn't found in the database, add it to the Link object
        else:
            link = Link(original_url=original_url, custom_url=custom_url)
            link.save()
            return render_template('link_added.html', new_link=link.custom_url, original_url=link.original_url)

    # check if the long url is already in the database
    link = Link.query.filter_by(original_url=original_url).first()

    # if it is, return the existing short url
    if link:
        return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url)
    
    # if it isn't, create a new Link object, save it, and return the new short url
    else:
        link = Link(original_url=original_url)
        link.save()
        return render_template('link_added.html', new_link=link.short_url, original_url=link.original_url)

    return ''


@short.route('/stats')
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def stats():
    links = Link.query.all()
    
    return render_template('stats.html', links=links)

@short.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

