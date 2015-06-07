from flask import Flask, render_template
from flask.ext.security import login_required, current_user
from flask.ext.principal import identity_loaded

from tacsite.config import BaseConfig
from tacsite.extensions import db, mail

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
  # security.init_app(app, user_datastore)
  # # manipulate principal
  # init_views(admin)
  # admin.init_app(app)

  app.register_blueprint(frontend)

  return app


def init_db_command(app=None):
    db.app = app
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
  app = create_app()
  init_db_command(app)
  app.run()