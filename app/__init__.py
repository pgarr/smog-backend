import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # loggers
    module_loggers = ['sqlalchemy', 'gios_api', 'notifier']

    # mail errors
    if not app.debug and not app.testing:  # TODO: odkomplikować tworzenie logów. Strategy/factory/builder pattern?
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='smog-backend failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)

            app.logger.addHandler(mail_handler)
            for logger_name in module_loggers:
                logger = logging.getLogger(logger_name)
                logger.addHandler(mail_handler)

        # stdout loggers
        if app.config['LOG_TO_STDOUT']:
            stdout_handler = logging.StreamHandler()
            stdout_handler.setLevel(logging.INFO)

            app.logger.addHandler(stdout_handler)
            for logger_name in module_loggers:
                logger = logging.getLogger(logger_name)
                logger.addHandler(stdout_handler)

        # file loggers
        else:
            formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
            if not os.path.exists('logs'):
                os.mkdir('logs')

            app_handler = RotatingFileHandler('logs/smog-api.log', maxBytes=102400, backupCount=100)
            app_handler.setFormatter(formatter)
            app.logger.addHandler(app_handler)

            for logger_name in module_loggers:
                module_handler = RotatingFileHandler('logs/' + logger_name + '.log', maxBytes=102400, backupCount=100)
                module_handler.setFormatter(formatter)
                logger = logging.getLogger(logger_name)
                logger.addHandler(module_handler)

        app.logger.setLevel(logging.INFO)

        app.logger.info('smog-backend startup')

    return app


from app import models
