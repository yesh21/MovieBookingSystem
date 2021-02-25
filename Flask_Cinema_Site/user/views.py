from Flask_Cinema_Site import app, db, models, mail
from Flask_Cinema_Site.helper_functions import get_redirect_url
from .forms import LoginForm, SignupForm

from flask import render_template, Blueprint, flash, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_mail import Message

from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer


user_blueprint = Blueprint(
    'user', __name__,
    template_folder='templates'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@login_manager.user_loader
def load_user(customerid):
    return models.Customer.query.get(int(customerid))


@user_blueprint.route('/', methods=['GET'])
def user():
    return render_template('user.html', title='User')


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template('login.html', title='Login', form=form)

    customer = db.session.query(models.Customer)\
        .filter(models.Customer.email.ilike(form.email.data)).first()

    if customer:
        if check_password_hash(customer.password, form.password.data):
            session['email'] = customer.email
            login_user(customer, remember=form.remember.data)
            return redirect(get_redirect_url())
        else:
            flash("incorrect password", 'danger')

    else:
        flash("email id not exists", "danger")
    return render_template('login.html', title='Login', form=form)


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if not form.validate_on_submit():
        return render_template('signup.html', title='Sign Up', form=form)

    hashed_password = generate_password_hash(form.password.data, method='sha256')
    new_user = models.Customer(username=form.username.data,
                               email=form.email.data,
                               password=hashed_password,
                               lastname=form.lastname.data,
                               firstname=form.firstname.data)
    db.session.add(new_user)
    db.session.commit()

    token = generate_confirmation_token(new_user.email)
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    html = render_template('activate.html', title='Activate Account', confirm_url=confirm_url)
    send_mail(new_user.email, token, html)

    flash("new account created", "success")
    return render_template('login.html', title='Login', form=form)


def send_mail(email, token, template, **kwargs):
    try:
        msg = Message('Thanks for registering!',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email],
                      html=template
                      )
        msg.body = 'An activation link from moviebox'
        mail.send(msg)
        return 'Sent'
    except IOError:
        print('plz set correct email and pass in config')
        return False


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


@user_blueprint.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for('user.signup'))
    email = confirm_token(token)
    user = models.Customer.query.filter_by(email=current_user.email).first_or_404()

    if email == user.email:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
        return redirect(url_for('user.signup'))

    flash("The confirmation link is invalid or has expired.", "warning")
    return redirect(url_for('user.login'))


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("successfully logged out!", "warning")
    return redirect(get_redirect_url())
