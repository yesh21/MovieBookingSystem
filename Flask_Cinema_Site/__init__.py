from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
# Load config
if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.ProductionConfig')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from Flask_Cinema_Site.home.views import home_blueprint
app.register_blueprint(home_blueprint)

from Flask_Cinema_Site.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')
