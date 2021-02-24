from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

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
mail = Mail(app)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap4')
admin.add_link(MenuLink(name='Logout', category='', url="/"))

from .models import Customer, CustomerViewing, Basket, BasketViewing, Viewing,\
                    Movie, ViewingSeat, Seat, Theatre

# Add administrative views here
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(CustomerViewing, db.session))
admin.add_view(ModelView(Basket, db.session))
admin.add_view(ModelView(BasketViewing, db.session))
admin.add_view(ModelView(Viewing, db.session))
admin.add_view(ModelView(Movie, db.session, endpoint='movies'))
admin.add_view(ModelView(ViewingSeat, db.session))
admin.add_view(ModelView(Seat, db.session))
admin.add_view(ModelView(Theatre, db.session))

from Flask_Cinema_Site.home.views import home_blueprint
app.register_blueprint(home_blueprint)

from Flask_Cinema_Site.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from Flask_Cinema_Site.movie.views import movies_blueprint
app.register_blueprint(movies_blueprint, url_prefix='/movie')
