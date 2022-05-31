import logging, os
from flask import Flask
from config import Config
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_moment import Moment




mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
login.login_view = 'auth.login'
login.login_message_category = "info"
app = Flask(__name__)

# define the name of your app below
APP_NAME = 'FYC'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'p17185722@gmail.com',
    "MAIL_PASSWORD": 'kdwrirsgmirarjuc'
}

app.config.update(mail_settings)
mail = Mail(app)

if __name__ == '__main__':
    with app.app_context():
        msg = Message(
                      sender='no-reply@' + app.config.get("p17185722@gmail.com"),
                      recipients=app.config['ADMINS'], subject=f'{APP_NAME} Failure',
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)

    # import the blueprint
    from app.auth.routes import auth
    from app.apps.routes import apps
    from app.staff.routes import staff
    from app.main.routes import main
    from app.errors.handlers import errors


    # register the blueprint
    app.register_blueprint(auth)
    app.register_blueprint(staff)
    app.register_blueprint(apps)
    app.register_blueprint(main)
    app.register_blueprint(errors)

# creates the error logs
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(f'logs/{APP_NAME.lower()}.log',
                                        maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info(f'{APP_NAME} startup')

    return app
