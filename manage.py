from tacsite.app import create_app
from flask.ext.security.utils import encrypt_password
from tacsite.extensions import db
from tacsite.models import PermissionNeed, user_datastore


def init_db_command(app):
    with app.app_context() as ctx:

        db.drop_all()
        db.create_all()

        users = [user_datastore.create_user(email='alex.flesch@web.de',
                                       password=encrypt_password('todo'), name='Admin'),
            user_datastore.create_user(email='marcel@quiqua.eu',
                                       password=encrypt_password('todo'), name='Admin')
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