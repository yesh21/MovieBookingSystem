from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class PaymentForm(FlaskForm):
    card = StringField('Card', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cvc = PasswordField('CVC', validators=[DataRequired()])
    submit = SubmitField('Pay')