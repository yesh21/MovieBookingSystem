import os


# Production
class DefaultConfig(object):
    DEBUG = False
    Testing = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'e327924a6b8846030dbd537a6a33c7f0f2149593b50bc235016e022846915444'

    # SAFE_URL_HOSTS = {'production-site.com'}


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECURITY_PASSWORD_SALT = 'uhh!secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yourid@gmail.com'
    MAIL_PASSWORD = 'yourpassword'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # click "allow less secure apps" in google for working


class ProductionConfig(DefaultConfig):
    SECRET_KEY = None
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECURITY_PASSWORD_SALT = 'uhh!secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'yourid@gmail.com'
    MAIL_PASSWORD = 'yourpassword'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    # click "allow less secure apps" in google for working
    SECRET_KEY = 'e327924a6b8846030dbd537a6a33c7f0f2149593b50bc235016e022846915444'


class TestConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}
