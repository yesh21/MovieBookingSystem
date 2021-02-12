# Production
class DefaultConfig(object):
    DEBUG = False
    Testing = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'e327924a6b8846030dbd537a6a33c7f0f2149593b50bc235016e022846915444'

    #SAFE_URL_HOSTS = {'production-site.com'}


class DevelopmentConfig(DefaultConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}


class ProductionConfig(DefaultConfig):
    SECRET_KEY = None


class TestConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SAFE_URL_HOSTS = {'127.0.0.1:5000'}