from datetime import datetime
import string
from random import choices
from .extensions import db

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(4), unique=True)
    custom_url = db.Column(db.String(50), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def save(self):
        db.session.add(self)
        db.session.commit()

    # Generate the short link
    def generate_short_link(self):
        chars = string.ascii_letters + string.digits
        short_url = ''.join(choices(chars, k=4))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()
        
        return short_url