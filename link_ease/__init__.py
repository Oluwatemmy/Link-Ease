from flask import Flask
from .main.routes import main
from dotenv import load_dotenv
from .users.routes import users
from .links.routes import links
from .models import User
from .settings import config_dict
from .links.routes import cache, limiter
from .errors.handlers import errors
from .extensions import db, bcrypt, login_manager, migrate


login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    load_dotenv()

    limiter.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(links)

    return app