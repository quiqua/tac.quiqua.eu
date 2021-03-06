# -*- coding: utf-8 -*-

import os

class BaseConfig(object):
  BASEDIR = os.path.abspath(os.path.dirname(__file__))
  PROJECT_NAME = 'TACSite'

  LOG_FOLDER = BASEDIR

  DEBUG = True

  SECRET_KEY = 'dTash$8d6V$§28(!cjNanDI9=&hs"2'
  ADMINS = ['youremail@yourdomain.com']

  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, 'data-dev.sqlite')

  MAIL_SERVER = 'mail.yourdomain.com'
  MAIL_PORT = 587
  MAIL_USE_SSL = False
  MAIL_USE_TLS = True

  MAIL_USERNAME = 'username'
  MAIL_PASSWORD = 'password'
  MAIL_DEFAULT_SENDER = ("Mailer", "mail.yourdomain.com")

  # Flask-Security Flags
  SECURITY_URL_PREFIX = '/auth' # namespace for login/register/....
  SECURITY_PASSOWRDLESS = False # Default
  SECURITY_CONFIRMABLE = False # Shall users confirm their identity?
  SECURITY_REGISTERABLE = False # Shall users register?
  SECURITY_RECOVERABLE = False # Shall users recover their credentials?
  SECURITY_TRACKABLE = True

  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "$2a$12$ELw877zXb0hSRCSOzH7Y3."
  SECURITY_CONFIRM_SALT = "$2a$12$fuk4XZZ4Dlw4G5orplyP2e"
  SECURITY_RESET_SALT = "$2a$12$.2lk2nOAyQyoav//kd6sN."
  SECURITY_REMEMBER_SALT = "$2a$12$V0.A1kBOd7RqbLoPCZeHxO"

class ProductionConfig(BaseConfig):
  DEBUG = False
  PROPAGATE_EXCEPTIONS = True
