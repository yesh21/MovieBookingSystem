from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


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
