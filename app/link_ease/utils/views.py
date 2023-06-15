import os
import hashlib
import requests
from PIL import Image
from io import BytesIO
from ..models import Link
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


def generate_qr_code(data, filename):
    api_key = "Q-nlMpQiPGh8CsU8D06Lx3ACZ8WyYIMsNjKVbpAA-PUV7EndZgqTX21xgcoyHXSM"
    url = f"https://api.qrcode-monkey.com/qr/custom?size=300&data={data}&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        # Open the image from the response content
        img = Image.open(BytesIO(response.content))

        # Save the image to a file
        image_folder = "C://Users//User//Desktop//Repos//Scissors//app//link_ease//static//image"
        # Generate a unique filename for the image based on the URL
        # url_hash = hashlib.md5(url.encode()).hexdigest()
        
        image_filename = f"qr_code_{filename}.png"
        image_path = os.path.join(image_folder, image_filename)
        img.save(image_path)

        return image_filename
        
    else:
        return None
