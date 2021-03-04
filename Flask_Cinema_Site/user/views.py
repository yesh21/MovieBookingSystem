from Flask_Cinema_Site import app, db, models, helper_functions
from Flask_Cinema_Site.models import Customer
from Flask_Cinema_Site.helper_functions import get_redirect_url
from .forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_api import status

from datetime import datetime

user_blueprint = Blueprint(
    'user', __name__,
    template_folder='templates'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@login_manager.user_loader
def load_user(customer_id):
    return Customer.query.get(int(customer_id))


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    helper_functions.send_email(
        subject='[Microblog] Reset Your Password',
        sender=app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reset_password_body.txt', user=user, token=token),
        html_body=render_template('email/reset_password_body.html', user=user, token=token)
    )


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    u = Customer.verify_reset_password_token(token)
    if not u:
        flash('Invalid reset password link', 'danger')
        return redirect(get_redirect_url())

    form = ResetPasswordForm()
    if not form.validate_on_submit():
        return render_template('reset_password.html', form=form)

    u.set_password(form.password.data)
    db.session.commit()

    flash('Password updated successfully', 'success')
    return redirect(url_for('user.login_get'))


@user_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        customer = db.session.query(models.Customer) \
            .filter_by(email=form.email.data).first()
        if not customer:
            flash('Unknown email has been entered.', 'danger')
        else:
            send_password_reset_email(customer)
            flash('A link has been sent to your email to reset your password'
                  ', the link will expire after 24 hours.', 'success')
    return render_template('forgot_password.html', title='Reset password', form=form)


@user_blueprint.route('/', methods=['GET'])
def user():
    return render_template('user.html', title='User')


@user_blueprint.route('/login', methods=['GET'])
def login_get():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@user_blueprint.route('/login', methods=['POST'])
def login_post():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = LoginForm()

    # Validate form submission
    if not form.validate_on_submit():
        return render_template('login.html', title='Login', form=form), status.HTTP_400_BAD_REQUEST

    # Check for user
    u = Customer.query.filter_by(email=form.email.data).first()
    if not u or not u.check_password(form.password.data):
        flash('Login failed. Provided details were incorrect.', 'danger')
        return render_template('login.html', title='Login', form=form), status.HTTP_400_BAD_REQUEST

    # Login successful
    login_user(u, form.remember.data)
    flash('Login successful', 'success')

    # Update last login date time
    u.last_login = datetime.now()
    db.session.commit()

    return redirect(get_redirect_url())


@user_blueprint.route('/signup', methods=['GET'])
def signup_get():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = SignupForm()
    return render_template('signup.html', title='Sign Up', form=form)


@user_blueprint.route('/signup', methods=['POST'])
def signup_post():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = SignupForm()

    if not form.validate_on_submit():
        return render_template('signup.html', title='Sign Up', form=form), status.\
            HTTP_400_BAD_REQUEST

    new_user = models.Customer(username=form.username.data,
                               email=form.email.data,
                               lastname=form.lastname.data,
                               firstname=form.firstname.data)
    new_user.set_password(form.password.data)

    db.session.add(new_user)
    db.session.commit()

    # Generate and send confirmation email
    token = new_user.get_email_confirm_token()
    confirm_url = url_for('user.confirm_email', token=token, _external=True)

    helper_functions.send_email(
        subject='Confirm your account',
        sender=app.config['MAIL_USERNAME'],
        recipients=[new_user.email],
        text_body=render_template('email/confirm_email_body.txt', confirm_url=confirm_url),
        html_body=render_template('email/confirm_email_body.html', confirm_url=confirm_url)
    )

    flash("new account created", "success")
    return redirect(url_for('user.login_get'))


@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    u = Customer.verify_email_confirm_token(token)
    if u.confirmed:
        flash("Account already confirmed.", "danger")
        return redirect(get_redirect_url())

    u.confirmed = True
    db.session.commit()
    flash(f'User [{u.username}] has been successfully confirmed', "success")
    return redirect(get_redirect_url())


@login_required
@user_blueprint.route('/activate')
def activate():
    return render_template('verify_account.html')


@login_required
@user_blueprint.route('/resend')
def resend():
    # Generate and send confirmation email
    token = current_user.get_email_confirm_token()
    confirm_url = url_for('user.confirm_email', token=token, _external=True)
    helper_functions.send_email(
        subject='Confirm your account',
        sender=app.config['MAIL_USERNAME'],
        recipients=[current_user.email],
        text_body=render_template('email/confirm_email_body.txt', confirm_url=confirm_url),
        html_body=render_template('email/confirm_email_body.html', confirm_url=confirm_url)
    )
    flash("Activation link sent!", "warning")
    return redirect(url_for('user.activate'))


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("successfully logged out!", "warning")
    return redirect(get_redirect_url())


@user_blueprint.route('/test', methods=['GET'])
def user_test():
    return render_template('email/reset_password_body.html', title='User')
