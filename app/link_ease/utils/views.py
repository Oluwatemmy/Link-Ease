from functools import wraps
from urllib.parse import urlparse
from flask import redirect, url_for
from datetime import timedelta, datetime
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
                return redirect(url_for('short.login', expired=True))
        return f(*args, **kwargs)
    return decorated_function
