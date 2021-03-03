from Flask_Cinema_Site import db, models, bcrypt

from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember me')
    login_btn = SubmitField('Login')


class SignupForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('Last name', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder": "Last Name"})

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Invalid email'),
                                             Length(min=3, max=70)],
                        render_kw={"placeholder": "Email"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min=3),
                                                     EqualTo('confirm_password',
                                                             message='Passwords must match')],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()],
                                     render_kw={"placeholder": "Confirm Password"})

    consent = BooleanField('I consent for storing all my data securely, including passwords',
                           validators=[DataRequired()])
    signup_btn = SubmitField('Register')

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        userdata = db.session\
            .query(models.Customer)\
            .filter(models.Customer.username.ilike(self.username.data))\
            .first()
        if userdata:
            raise ValidationError(f" Username ['{userdata.username}'] already exists")
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character '{char}' is not allowed in username.")

    def validate_email(self, email):
        userdata = db.session\
            .query(models.Customer)\
            .filter(models.Customer.email.ilike(self.email.data))\
            .first()
        if userdata:
            raise ValidationError(f"Email '{userdata.email}' already exists")


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')],
                        render_kw={"placeholder": "Email"})
    submit = SubmitField('Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),
                              EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])

    password = PasswordField('New Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Save')

    def validate_current_password(self, current_password):
        if current_user.check_password(current_password.data):
            return

        raise ValidationError('Incorrect password')
