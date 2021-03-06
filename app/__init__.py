from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.pusher import Pusher

# extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
moment = Moment()
pusher = Pusher()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.app_context().push()
    db.init_app(app)
    
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    pusher.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.core import bp as core_bp
    app.register_blueprint(core_bp)

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix="/chat")

    from app.setup import bp as setup_bp
    app.register_blueprint(setup_bp, url_prefix="/setup")

    return app

from app import models