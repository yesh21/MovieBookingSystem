from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class PaymentForm(FlaskForm):
    card = StringField('Card', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cvc = PasswordField('CVC', validators=[DataRequired()])
    submit = SubmitField('Pay')
