from flask import render_template, Blueprint, flash, session, redirect, url_for
from Flask_Cinema_Site import app
from Flask_Cinema_Site import db, models, mail
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, SignupForm
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home.login'


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
                login_user(customer, remember=form.remember.data)
                return 'logged in'
            else:
                flash("incorrect password", 'error')

        else:
            flash("email id not exists", "error")
    return render_template('login.html', form=form)


@home_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,
                                                 method='sha256')
        new_user = models.Customer(username=form.username.data,
                                   email=form.email.data,
                                   password=hashed_password,
                                   lastname=form.lastname.data,
                                   firstname=form.firstname.data)
        db.session.add(new_user)
        db.session.commit()
        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('home.confirm_email',
                              token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        send_mail(new_user.email, token, html)
        flash("new account created", "update")
        return render_template('login.html', form=form)

    return render_template('signup.html', form=form)


def send_mail(email, token, template, **kwargs):
    msg = Message('Thanks for registering!',
                  sender='yourownid@gmail.com',
                  recipients=[email],
                  html=template
                  )
    msg.body = 'An activation link from moviebox'
    mail.send(msg)
    return 'Sent'


def confirm_token(token, expiration=360000):
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except token.invalid:
        return False
    return email


def generate_confirmation_token(email):
    serializer = Serializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


@home_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash("Account already confirmed.", "update")
        return redirect(url_for('home.signup'))
    email = confirm_token(token)
    user = models.Customer.query.filter_by(email=current_user
                                           .email).first_or_404()
    if email == user.email:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "update")
        return redirect(url_for('home.signup'))
    else:
        flash("The confirmation link is invalid or has expired.", "warning")
        return redirect(url_for('home.login'))
    return redirect(url_for('home.signup'))


@home_blueprint.route('/logout')
def logout():
    logout_user()
    flash("successfully logged out!", "warning")
    return redirect(url_for('home.login'))
