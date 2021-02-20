from flask import render_template, Blueprint, flash, session, redirect, url_for
from Flask_Cinema_Site import app
from Flask_Cinema_Site import db, models
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash
from .forms import LoginForm


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@home_blueprint.route('/', methods=['GET'])
def user():
    return render_template('user.html')


@login_manager.user_loader
def load_user(customerid):
    return models.Customer.query.get(int(customerid))


@home_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        customer = db.session.query(models.Customer
                                    ).filter(models.Customer
                                             .email.ilike(form.
                                                          email.data)).first()
        if customer:
            if check_password_hash(customer.password, form.password.data):
                session['email'] = customer.email
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                flash("incorrect password")

        else:
            flash("email id not exists")
    return render_template('login.html', form=form)
