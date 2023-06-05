from flask import Flask
from .routes import cache, limiter

from .extensions import db, bcrypt, login_manager, migrate
from .routes import short


login_manager.login_view = 'short.login'

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    limiter.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(short)

    return app