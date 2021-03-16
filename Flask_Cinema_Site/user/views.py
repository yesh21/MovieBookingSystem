from Flask_Cinema_Site import app, db, models, helper_functions
from Flask_Cinema_Site.models import Customer
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.forms import SimpleForm
from .forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm, \
    ChangePasswordForm, ChangeDetailsForm

from Flask_Cinema_Site.decorators import check_confirmed
from flask import render_template, Blueprint, flash, redirect, url_for, request, current_app, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_api import status
from flask_principal import identity_changed, Identity, AnonymousIdentity

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


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='Login', form=form)

    # Validate form submission
    if not form.validate_on_submit():
        return render_template('login.html', title='Login', form=form), status.HTTP_400_BAD_REQUEST

    # Check for user
    u = Customer.query.filter_by(email=form.email.data).first()
    if not u or not u.check_password(form.password.data):
        flash('Login failed. Provided details were incorrect.', 'danger')
        return render_template('login.html', title='Login', form=form), status.HTTP_400_BAD_REQUEST

    # Update last login date time
    u.last_login = datetime.now()
    db.session.commit()

    # Login successful
    login_user(u, form.remember.data)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    flash('Login successful', 'success')
    return redirect(get_redirect_url())


@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # Check if user logged in
    if current_user.is_authenticated:
        return redirect(get_redirect_url())

    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', title='Sign Up', form=form)

    if not form.validate_on_submit():
        return render_template('signup.html', title='Sign Up', form=form), status.\
            HTTP_400_BAD_REQUEST

    new_user = models.Customer(first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               username=form.username.data,
                               email=form.email.data)
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

    flash(f'New user \'{new_user.username}\' was successfully created', 'success')
    return redirect(url_for('user.login'))


@user_blueprint.route('/confirm/<token>')
def confirm_email(token):
    u = Customer.verify_email_confirm_token(token)
    if u.confirmed:
        flash("Account already confirmed.", "danger")
        return redirect(get_redirect_url())

    u.confirmed = True
    db.session.commit()
    flash(f'User \'{u.username}\' has been successfully confirmed', "success")
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


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if not current_user.is_authenticated:
        flash('Logout failed. No user logged in', 'danger')
        return redirect(get_redirect_url())

    form = SimpleForm()
    del form.id
    if not form.validate_on_submit():
        flash('Logout failed', 'danger')
        return redirect(url_for('home.home'))

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('home.home'))


def render_manage_user(change_details_form=None, change_password_form=None,
                       res_status=status.HTTP_200_OK):
    if change_details_form is None:
        change_details_form = ChangeDetailsForm()
        # Initialize form
        change_details_form.first_name.data = current_user.first_name
        change_details_form.last_name.data = current_user.last_name
        change_details_form.username.data = current_user.username
        change_details_form.email.data = current_user.email
    if change_password_form is None:
        change_password_form = ChangePasswordForm()

    return render_template('manage_user.html', title='Manage Account',
                           details_form=change_details_form,
                           password_form=change_password_form), res_status


@user_blueprint.route('/manage')
@login_required
@check_confirmed
def manage():
    return render_manage_user()


@user_blueprint.route('/manage/update_user_details', methods=['POST'])
@login_required
def update_user_details():
    form = ChangeDetailsForm()

    # Validate submitted details
    if not form.validate_on_submit():
        return render_manage_user(change_details_form=form, res_status=status.HTTP_400_BAD_REQUEST)

    # Update details
    current_user.confirmed = current_user.confirmed and current_user.email == form.email.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()

    flash('Details successfully updated', 'success')

    return render_manage_user(change_details_form=form)


@user_blueprint.route('/manage/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if not form.validate_on_submit():
        return render_manage_user(change_password_form=form, res_status=status.HTTP_400_BAD_REQUEST)

    # Update password
    current_user.set_password(form.password.data)
    db.session.commit()
    flash('Password updated successfully', 'success')
    return render_manage_user(change_password_form=form)
