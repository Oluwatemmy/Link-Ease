from flask import Blueprint, render_template, url_for, request, redirect
from .models import Link, User
from .extensions import db, bcrypt
import validators
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required, current_user, login_user, logout_user

# Create the limiter and cache objects
limiter = Limiter(get_remote_address)
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
        
    # check if the original_url is already in the database and does not have a custom url
    short_link = Link.query.filter_by(original_url=original_url, custom_url=None).first()

    # if it is, return the existing short url
    if short_link:
        return render_template('link_added.html', new_link=short_link.short_url, original_url=short_link.original_url)
    
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


@short.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password and confirm password match
        if password != confirm_password:
            return render_template('register.html', password_match=False, error_message='Passwords do not match')
        
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', email_exists=True, error_message='Email already in use')
        # hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # create a new user object
        user = User(name=name, email=email, password=hashed_password)
        # save the user object
        user.save()
        return redirect(url_for('short.login'))

    return render_template('register.html')


@short.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')
