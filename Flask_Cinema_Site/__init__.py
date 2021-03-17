from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_principal import Principal
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_cors import CORS

app = Flask(__name__)
# Load config
app.config['CORS_HEADERS'] = 'Content-Type'
if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.ProductionConfig')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
cors = CORS(app)

# User roles
principals = Principal(app)
from Flask_Cinema_Site.roles import customer_permission, manager_permission, admin_permission
app.jinja_env.globals.update(is_customer=customer_permission.can,
                             is_manager=manager_permission.can,
                             is_admin=admin_permission.can)

# Add administrative views here
from .models import User, UserRole, Role, UserViewing, Basket, BasketViewing, Viewing,\
    Movie, ViewingSeat, Seat, Theatre

admin = Admin(app, name='microblog', template_mode='bootstrap4')
admin.add_link(MenuLink(name='Logout', category='', url="/"))
admin.add_view(ModelView(User, db.session, endpoint='user_'))
admin.add_view(ModelView(UserRole, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserViewing, db.session))
admin.add_view(ModelView(Basket, db.session))
admin.add_view(ModelView(BasketViewing, db.session))
admin.add_view(ModelView(Viewing, db.session))
admin.add_view(ModelView(Movie, db.session, endpoint='movies'))
admin.add_view(ModelView(ViewingSeat, db.session))
admin.add_view(ModelView(Seat, db.session))
admin.add_view(ModelView(Theatre, db.session))
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Add custom functions to all templates
from Flask_Cinema_Site.helper_functions import get_field_html, get_field_group_html, \
    get_file_upload_group_html, get_file_upload_errors_html
app.jinja_env.globals.update(get_field_html=get_field_html,
                             get_field_group_html=get_field_group_html,
                             get_file_upload_group_html=get_file_upload_group_html,
                             get_file_upload_errors_html=get_file_upload_errors_html)

# Add simple form to all templates
from Flask_Cinema_Site.forms import SimpleForm


@app.context_processor
def inject_simple_form():
    return dict(simple_form=SimpleForm())


# Register blueprints / views
from Flask_Cinema_Site.errors.views import unauthorized, not_found

from Flask_Cinema_Site.home.views import home_blueprint
app.register_blueprint(home_blueprint)

from Flask_Cinema_Site.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from Flask_Cinema_Site.movie.views import movies_blueprint
app.register_blueprint(movies_blueprint, url_prefix='/movie')

from Flask_Cinema_Site.bookings.views import bookings_blueprint
app.register_blueprint(bookings_blueprint, url_prefix='/book')
