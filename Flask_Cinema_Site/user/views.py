from Flask_Cinema_Site import app, db, models, mail
from Flask_Cinema_Site.helper_functions import get_redirect_url
from .forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm

from flask import render_template, Blueprint, flash, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_mail import Message

from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from threading import Thread


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


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['MAIL_USERNAME'][0],
               recipients=[user.email],
               text_body=render_template('reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('reset_password.txt',
                                         user=user, token=token))


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pass
    return render_template('reset_password.html', form=form)


@user_blueprint.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        customer = db.session.query(models.Customer)\
            .filter_by(email=form.email.data).first()
        if not customer:
            flash('Unknown email has been entered.', 'danger')
        else:
            send_password_reset_email(customer)
            flash('A link has been sent to your email to reset your password, \
                the link will expire after 24 hours.', 'success')
    return render_template('forgot_password.html', title='Reset password', form=form)


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
