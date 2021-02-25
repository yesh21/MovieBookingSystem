from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from Flask_Cinema_Site import db, models


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Invalid email')
                                             ], render_kw={
                                                 "placeholder": "Email"})
    password = PasswordField('Password',
                             validators=[DataRequired(
                             )], render_kw={
                                 "placeholder": "Password"})
    remember = BooleanField('remember me')
    loginbtn = SubmitField('Login')


class SignupForm(FlaskForm):
    firstname = StringField('firstname',
                            validators=[DataRequired(), Length(min=3, max=20)],
                            render_kw={"placeholder": "First Name"})
    lastname = StringField('lastname',
                           validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder": "Last Name"})
    username = StringField('username',
                           validators=[DataRequired(),
                                       Length(min=3, max=20)],
                           render_kw={"placeholder": "username"})
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(message='Invalid email'),
                                    Length(min=3, max=70)],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              Length(min=3, max=20),
                              validators.EqualTo('confirmPassword',
                              message='Passwords must match')],
                             render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField('ConfirmPassword',
                                    validators=[DataRequired()],
                                    render_kw={"placeholder":
                                               "Confirm Password"})
    consent = BooleanField('consent',
                           validators=[DataRequired()])
    Signupbtn = SubmitField('Signup')

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        userdata = db.session.query(models.Customer
                                    ).filter(models.Customer.username.
                                             ilike(self.username.data)).first()
        if userdata:
            raise ValidationError(
                  f" Username '{userdata.username}'   already exists")
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    def validate_email(self, email):
        userdata = db.session.query(models.Customer
                                    ).filter(models.Customer.email.
                                             ilike(self.email.data)).first()
        if userdata:
            raise ValidationError(
                  f"Email '{userdata.email}' already exists")
