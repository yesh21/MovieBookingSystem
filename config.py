import os


# Copied to all configs
class DefaultConfig(object):
    # Flask
    DEBUG = False
    Testing = False

    # SQLAlchemy
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'e327924a6b8846030dbd537a6a33c7f0f2149593b50bc235016e022846915444'

    # Flask mail
    # click "allow less secure apps" in google for working
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USERNAME = 'yourid@gmail.com'
    # MAIL_PASSWORD = 'yourpassword'
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # Plz no spam
    MAIL_SERVER = 'ssl0.ovh.net'
    MAIL_PORT = 465
    MAIL_USERNAME = 'comp2913-group40@aaronrosser.xyz'
    MAIL_PASSWORD = 'hIYcrp3Rxg61OwJ'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Check redirect links
    # SAFE_URL_HOSTS = {'production-site.com'}

    # Bcrypt?
    SECURITY_PASSWORD_SALT = 'uhh!secret'


class DevelopmentConfig(DefaultConfig):
    # Flask
    DEBUG = True

    # Check redirect links
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}


class ProductionConfig(DefaultConfig):
    pass


class TestConfig(DefaultConfig):
    # Flask
    TESTING = True

    # Flask-WTF
    WTF_CSRF_ENABLED = False

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    # Check redirect links
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}
