from flask import Flask

from flask.ext.security.utils import encrypt_password
from tacsite.config import BaseConfig
from tacsite.extensions import db, mail, security
from tacsite.models import PermissionNeed, user_datastore
#from flasky.extensions import db, security, admin
from tacsite.views import frontend


def has_errors(fields):
    for field in fields:
        if field.errors:
            return True
    return False

def create_app():
    app = Flask(__name__)
    app.config.from_object(BaseConfig)
    app.jinja_env.globals['enumerate'] = enumerate
    app.jinja_env.globals['has_errors'] = has_errors
    db.init_app(app)
    mail.init_app(app)
    security.init_app(app, user_datastore)
    # # manipulate principal
    # init_views(admin)
    # admin.init_app(app)

    app.register_blueprint(frontend)

    return app


def init_db_command(app):
    with app.app_context() as ctx:

        db.drop_all()
        db.create_all()

        users = [user_datastore.create_user(email='alex.flesch@web.de',
                                       password=encrypt_password('!HaLlo123TAC'), name='Admin'),
            user_datastore.create_user(email='marcel@quiqua.eu',
                                       password=encrypt_password('tAcBeRlIn!$'), name='Admin')
        ]

        roles = [
            user_datastore.create_role(name='admin', description='Admin')
        ]

        permissions = [
            PermissionNeed(method='role', value='read'),
            PermissionNeed(method='role', value='write'),
            PermissionNeed(method='role', value='update'),
            PermissionNeed(method='role', value='delete'),
        ]

        db.session.add_all(roles)
        db.session.add_all(permissions)
        for usr in users:
            usr.roles.append(roles[0])

        for p in permissions:
            roles[0].permission_need.append(p)

        db.session.add_all(users)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    init_db_command(app)
    app.run()