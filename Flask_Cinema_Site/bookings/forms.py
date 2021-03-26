from Flask_Cinema_Site.models import Seat, TicketType

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, ValidationError

import json


class CashPaymentForm(FlaskForm):
    seats_json = HiddenField('Selected Seats', validators=[DataRequired()])
    customer_email = EmailField('Customer email', validators=[DataRequired(), Email()])
    submit = SubmitField('Accept payment and book')

    def validate_seats_json(self, seats_json):
        seats = json.loads(self.seats_json.data)

        for seat_num, ticket_type in seats:
            if not Seat.is_number_valid(seat_num):
                raise ValidationError(f'Seat \'{seat_num}\' is invalid')

            t = TicketType.query.filter_by(name=ticket_type).first()
            if not t:
                raise ValidationError(f'Ticket type \'{ticket_type}\' not found')


class PaymentForm(FlaskForm):
    card = StringField('Card', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cvc = PasswordField('CVC', validators=[DataRequired()])
    submit = SubmitField('Pay')
