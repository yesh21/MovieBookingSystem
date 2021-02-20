from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
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


class SignupForm(Form):
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
