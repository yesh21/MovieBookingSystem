from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_principal import Principal
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

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

# User roles
principals = Principal(app)
from Flask_Cinema_Site.roles import customer_permission, manager_permission, admin_permission
app.jinja_env.globals.update(is_customer=customer_permission.can,
                             is_manager=manager_permission.can,
                             is_admin=admin_permission.can)

# Add administrative views here
from .models import User, UserRole, Role, Viewing, Transaction, Movie, Seat, Screen, TicketType

# Only allow admin view in development
if app.config['ENV'] == 'development':
    admin = Admin(app, name='microblog', template_mode='bootstrap4')
    admin.add_link(MenuLink(name='Logout', category='', url="/"))
    admin.add_view(ModelView(User, db.session, endpoint='user_'))
    admin.add_view(ModelView(UserRole, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Transaction, db.session))
    admin.add_view(ModelView(Viewing, db.session))
    admin.add_view(ModelView(Movie, db.session, endpoint='movies'))
    admin.add_view(ModelView(Seat, db.session))
    admin.add_view(ModelView(TicketType, db.session))
    admin.add_view(ModelView(Screen, db.session))
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Add custom filters
from Flask_Cinema_Site.jinja2.filters import format_datetime_generator
app.jinja_env.filters['format_datetime'] = format_datetime_generator

# Add custom functions to all templates
from Flask_Cinema_Site.jinja2.functions import get_field_html, get_field_group_html, \
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
app.register_blueprint(home_blueprint, url_prefix='/home')

from Flask_Cinema_Site.user.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from Flask_Cinema_Site.movie.views import movies_blueprint
app.register_blueprint(movies_blueprint, url_prefix='/movie')

from Flask_Cinema_Site.bookings.views import bookings_blueprint
app.register_blueprint(bookings_blueprint, url_prefix='/booking')

from Flask_Cinema_Site.analysis.views import analysis_blueprint
app.register_blueprint(analysis_blueprint, url_prefix='/analysis')
