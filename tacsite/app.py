import os

from flask import Flask, render_template

from flask.ext.security.utils import encrypt_password
from tacsite.config import BaseConfig, ProductionConfig
from tacsite.extensions import db, mail, security
from tacsite.models import PermissionNeed, user_datastore
#from flasky.extensions import db, security, admin
from tacsite.views import frontend


def has_errors(fields):
    for field in fields:
        if field.errors:
            return True
    return False

def create_app(production=False):
    app = Flask(__name__)
    if production:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(BaseConfig)
    app.jinja_env.globals['enumerate'] = enumerate
    app.jinja_env.globals['has_errors'] = has_errors
    db.init_app(app)
    mail.init_app(app)
    security.init_app(app, user_datastore)
    app.register_blueprint(frontend)

    configure_error_handlers(app)
    configure_logging(app)

    return app


def configure_error_handlers(app):
    # HTTP error pages definitions

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/forbidden_page.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/page_not_found.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template('errors/method_not_allowed.html'), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/server_error.html'), 500

def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    #from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'info.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')