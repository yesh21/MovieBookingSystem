from Flask_Cinema_Site.models import Seat, TicketType

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, ValidationError

import json


class BasePaymentForm(FlaskForm):
    seats_json = HiddenField('Selected Seats', validators=[DataRequired()])

    def validate_seats_json(self, seats_json):
        seats = json.loads(self.seats_json.data)

        for seat_num, ticket_type in seats:
            if not Seat.is_number_type_valid(seat_num, ticket_type):
                raise ValidationError(f'Seat \'{seat_num}\' with type \'{ticket_type}\' is invalid')


class CashPaymentForm(BasePaymentForm):
    customer_email = EmailField('Customer email', validators=[DataRequired(), Email()])
    submit = SubmitField('Accept payment and book')


class CardPaymentForm(BasePaymentForm):
    card = StringField('Card', validators=[DataRequired(), Length(min=2, max=20)])
    cvc = PasswordField('CVC', validators=[DataRequired()])
    submit = SubmitField('Pay')
