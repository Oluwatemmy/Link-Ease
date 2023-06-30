import secrets
import smtplib
import qrcode, io
from functools import wraps
from urllib.parse import urlparse
from flask import redirect, url_for
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from flask_login import current_user, logout_user


def url_validate(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    

def fresh_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # check if the session has expired
            session_timeout = timedelta(hours=5)
            expiration_time = current_user.last_seen + session_timeout
            if datetime.utcnow() > expiration_time:
                logout_user()
                return redirect(url_for('users.login', expired=True))
        return f(*args, **kwargs)
    return decorated_function


def generate_qr_code(url):
    img = qrcode.make(url)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


def generate_reset_token(length):
    return secrets.token_hex(length)


def send_email(user_mail, reset_link):
    sender = "temmyvibez15@gmail.com"
    password = "lghbvsjfldnzitym"
    subject = "Password Reset Request"
    content = f'''
        <p>Hello {user_mail.username},</p>
        <p>We have received a request to reset your password. To proceed with the password reset, please click on the link below:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>If you did not initiate this request, please ignore this email. Your password will not be changed.</p>
        <p>Thank you,</p>
        <p>Link-Ease Team</p>
    '''

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = user_mail.email
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))

    # Create the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    # Send the email
    server.sendmail(sender, user_mail.email, message.as_string())
    server.quit()
