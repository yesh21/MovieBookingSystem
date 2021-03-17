from Flask_Cinema_Site import db, models
from Flask_Cinema_Site.models import User

from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    login_btn = SubmitField('Login')


class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=3, max=User.first_name.type.length)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=3, max=User.last_name.type.length)])

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=User.username.type.length)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=User.email.type.length)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=3),
                                                     EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])

    consent = BooleanField('I consent for storing all my data securely, including passwords',
                           validators=[DataRequired()])
    signup_btn = SubmitField('Register')

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        userdata = db.session\
            .query(models.User)\
            .filter(models.User.username.ilike(self.username.data))\
            .first()
        if userdata:
            raise ValidationError(f"Username '{userdata.username}' already exists")
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character '{char}' is not allowed in username.")

    def validate_email(self, email):
        userdata = db.session\
            .query(models.User)\
            .filter(models.User.email.ilike(self.email.data))\
            .first()
        if userdata:
            raise ValidationError(f"Email '{userdata.email}' already exists")


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email')],
                        render_kw={"placeholder": "Email"})
    submit = SubmitField('Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])

    password = PasswordField('New Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Save')

    def validate_current_password(self, current_password):
        if current_user.check_password(current_password.data):
            return

        raise ValidationError('Incorrect password')


class ChangeDetailsForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(min=3, max=User.first_name.type.length)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=3, max=User.last_name.type.length)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=User.username.type.length)])
    email = EmailField('Email', validators=[DataRequired(), Length(max=User.email.type.length), Email()])

    submit = SubmitField('Save')

    # Check email is not already taken by another user
    def validate_email(self, email):
        if email.data == current_user.email:
            return

        u = User.query.filter_by(email=email.data).first()
        if not u:
            return
        raise ValidationError('Email already registered to an account.')

    # Check username is not already taken by another user
    def validate_username(self, username):
        if username.data == current_user.username:
            return

        u = User.query.filter_by(username=username.data).first()
        if not u:
            return
        raise ValidationError('Username already registered to an account.')
