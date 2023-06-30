from link_ease.models import User
from ..extensions import db, bcrypt
from datetime import datetime, timedelta
from ..utils.views import generate_reset_token, send_email
from flask_login import login_user, current_user, logout_user
from flask import render_template, url_for, flash, redirect, request, Blueprint


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        elif len(username) < 2:
            # flash a message to the user
            flash('Username must be greater than 2 characters.', 'danger')
            return render_template('register.html', username_error=True, error_message='Username must be greater than 2 characters.')
        elif len(password) < 6:
            # flash a message to the user
            flash('Password must be greater than 6 characters.', 'danger')
            return render_template('register.html', password_error=True, error_message='Password must be greater than 6 characters.')
        
        # create a new user object and hash the password
        user = User(username=username, email=email)
        user.set_password(password)
        # save the user object
        user.save()
        # send a message to the user
        flash('You have successfully registered! Please log in.','success')
        return redirect(url_for('users.login'))

    return render_template('register.html')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            # flash a message to the user
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html')


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/reset-password', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
    
        email = request.form['email']

        user = User.query.filter_by(email=email).first()

        if user:
            # generate token and send the user an email
            token = generate_reset_token(25)
            user.password_reset_token = token
            user.password_reset_token_expiration = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()

            reset_link = url_for('users.password_reset', token=token, _external=True)  # Generate the reset link

            # send the user an email
            send_email(user, reset_link)

            # flash a message to the user
            flash('An email has been sent with instructions to reset your password.', 'info')

            return redirect(url_for('users.login'))
        
        # flash a message to the user
        flash('Email does not exist', 'danger')
        return render_template('password_reset_request.html', email_exists=False, error_message='Email does not exist')
    
    return render_template('password_reset_request.html')


@users.route('/reset-password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.query.filter_by(password_reset_token=token).first()

    if user is None:
        # flash a message to the user
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.password_reset_request'))
    
    # check if the password_reset_token_expiration is still valid
    if user.password_reset_token_expiration < datetime.utcnow():
        # flash a message to the user
        flash('The password reset token has expired', 'warning')
        return redirect(url_for('users.password_reset_request'))
    
    if request.method == 'POST':
        # Get the form data
        password = request.form['password']
        confirm_password = request.form['confirm_password']


        # Check if password and confirm password match
        if password == confirm_password:
            user.set_password(confirm_password)
            user.password_reset_token = None
            user.password_reset_token_expiration = None
            db.session.commit()

            # flash a message to the user
            flash('Your password has been updated! You are now able to log in','success')
            return redirect(url_for('users.login'))
        
        else:
            # flash a message to the user
            flash('Passwords do not match', 'danger')
            return render_template('password_reset.html', password_match=False, error_message='Passwords do not match')

    return render_template('password_reset.html', token=token)
