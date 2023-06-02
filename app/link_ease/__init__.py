from flask import Flask
from flask_migrate import Migrate
from .routes import cache, limiter

from .extensions import db
from .routes import short

migrate = Migrate()

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    limiter.init_app(app)

    cache.init_app(app)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(short)

    return app