from Flask_Cinema_Site.models import Seat, SavedCard

from flask_login import current_user
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, HiddenField, BooleanField
from wtforms.fields.html5 import EmailField, DateField
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
    card = StringField('Card', validators=[DataRequired(), Length(min=16, max=19)])
    cvc = PasswordField('CVC', validators=[DataRequired()])
    expiry = DateField('Expiry date')
    remember = BooleanField('Remember card')
    submit = SubmitField('Pay')

    def validate_card(self, card_number):
        if not self.card.data.startswith('****'):
            return

        last_4_digits = self.card.data[-4:]
        saved_card = SavedCard.query\
            .filter(SavedCard.user_id == current_user.id)\
            .filter(SavedCard.number.like(f'%{last_4_digits}'))\
            .first()
        if not saved_card:
            raise ValidationError(f'Card ending \'{last_4_digits}\' not found')
