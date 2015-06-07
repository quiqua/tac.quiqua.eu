# -*- coding: utf-8 -*-

import os

class BaseConfig(object):
  BASEDIR = os.path.abspath(os.path.dirname(__file__))
  PROJECT_NAME = 'TACSite'

  DEBUG = True

  SECRET_KEY = 'dTash$8d6V$§28(!cjNanDI9=&hs"2'

  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, 'data-dev.sqlite')


  MAIL_SERVER = 'mail.yourdomain.com'
  MAIL_PORT = 25
  MAIL_USE_SSL = False
  MAIL_USE_TLS = False
  MAIL_USERNAME = 'yourusername'
  MAIL_PASSWORD = 'yourpassword'
  DEFAULT_MAIL_SENDER = ("TAC Berlin", "mail.yourdomain.com")

  # Flask-Security Flags
  SECURITY_URL_PREFIX = '/auth' # namespace for login/register/....
  SECURITY_PASSOWRDLESS = False # Default
  SECURITY_CONFIRMABLE = False # Shall users confirm their identity?
  SECURITY_REGISTERABLE = True # Shall users register?
  SECURITY_RECOVERABLE = True # Shall users recover their credentials?
  SECURITY_TRACKABLE = True

  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "$2a$12$ELw877zXb0hSRCSOzH7Y3."
  SECURITY_CONFIRM_SALT = "$2a$12$fuk4XZZ4Dlw4G5orplyP2e"
  SECURITY_RESET_SALT = "$2a$12$.2lk2nOAyQyoav//kd6sN."
  SECURITY_REMEMBER_SALT = "$2a$12$V0.A1kBOd7RqbLoPCZeHxO"

class ProductionConfig(BaseConfig):
  DEBUG = False
  PROPAGATE_EXCEPTIONS = True
