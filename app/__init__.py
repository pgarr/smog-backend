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

    if not app.debug and not app.testing:  # TODO: dalej popracować nad tworzeniem logów. Wciąż zduplikowany kod
        # mail errors
        if app.config['MAIL_SERVER']:
            handler = set_stmp_handler(app.config, level=logging.ERROR)
            register_handler(app, module_loggers, handler)

        # stdout loggers
        if app.config['LOG_TO_STDOUT']:
            handler = set_stdout_logger(level=logging.INFO)
            register_handler(app, module_loggers, handler)

        # file loggers
        else:
            register_file_loggers(app, module_loggers)

        app.logger.setLevel(logging.INFO)

    return app


def set_stmp_handler(config, level=logging.ERROR):
    auth = None
    if config['MAIL_USERNAME'] or config['MAIL_PASSWORD']:
        auth = (config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
    secure = None
    if config['MAIL_USE_TLS']:
        secure = ()
    handler = SMTPHandler(
        mailhost=(config['MAIL_SERVER'], config['MAIL_PORT']),
        fromaddr='no-reply@' + config['MAIL_SERVER'],
        toaddrs=config['ADMINS'], subject='smog-backend failure',
        credentials=auth, secure=secure)
    handler.setLevel(level)

    return handler


def set_stdout_logger(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setLevel(level)
    return handler


def register_handler(app, module_loggers, handler):
    app.logger.addHandler(handler)
    for logger_name in module_loggers:
        logger = logging.getLogger(logger_name)
        logger.addHandler(handler)


def register_file_loggers(app, module_loggers):
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


from app import models
