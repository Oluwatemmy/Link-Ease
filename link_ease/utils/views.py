import os, tempfile, mimetypes
import qrcode, io, uuid
import secrets
import smtplib
import requests
from PIL import Image
from io import BytesIO
from functools import wraps
from ..models import Link
from urllib.parse import urlparse
from flask import redirect, url_for, request, Response
from email.mime.text import MIMEText
from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename


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


# def generate_qr_code(data, filename):
#     api_key = "Jl2ad5KcvEPPVo7IU1mTaxQPi2CfWMqGERAlZgz074jAk1yTtefOh9Uxo8jr14AI"
#     url = f"https://api.qrcode-monkey.com/qr/custom?size=300&data={data}&apiKey={api_key}"
#     response = requests.get(url)

#     if response.status_code == 200:
#         # Open the image from the response content
#         img = Image.open(BytesIO(response.content))

#         # Save the image to a file
#         image_folder = "C://Users//User//Desktop//Repos//Scissors//app//link_ease//static//image"
#         # Generate a unique filename for the image based on the URL
#         # url_hash = hashlib.md5(url.encode()).hexdigest()
        
#         image_filename = f"qr_code_{filename}.png"
#         image_path = os.path.join(image_folder, image_filename)
#         img.save(image_path, 'PNG')

#         return image_filename
        
#     else:
#         return None

# def generate_qr_code_image(url):
#     qr = qrcode.QRCode(
#         version=1,
#         box_size=10,
#         border=5
#     )

#     qr.add_data(url)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")

#     # Convert the image to bytes
#     img_bytes = io.BytesIO()
#     img.save(img_bytes, format='PNG')
#     img_bytes.seek(0)

#     # Generate a unique filename for the image
#     filename = secure_filename(f"{uuid.uuid4()}.png")

#     # Get the mimetype of the image
#     mimetype = 'image/png'

#     return img_bytes, mimetype, filename


#     # # Create a temporary file to save the image
#     # with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
#     #     # Save the image to the temporary file
#     #     img.save(temp_file.name)

#     #     # Get the filename of the saved image
#     #     img_name = os.path.basename(temp_file.name)
    
#     # filename = secure_filename(img_name)
#     # mimetype, _ = mimetypes.guess_type(filename)

#     # image = Img(image=img.read(), mimetype=mimetype, name=filename)
#     # image.save()
    
#     # return image

#     # # Convert the image to binary data
#     # img_buffer = BytesIO()
#     # img.save(img_buffer, format='PNG')
#     # img_buffer.seek(0)
#     # img_binary = img_buffer.read()

#     # # qrcode_image = Link(qr_code_image=img_binary)
#     # # qrcode_image.save()

#     # return img_binary


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

