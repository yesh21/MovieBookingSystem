from flask import render_template, redirect, Blueprint, flash, send_file
from flask_login import current_user, login_required

from Flask_Cinema_Site import db
from Flask_Cinema_Site.roles import manager_permission
from Flask_Cinema_Site.models import Viewing, Transaction, TicketType, SavedCard, Seat
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.bookings.forms import CardPaymentForm, CashPaymentForm
from Flask_Cinema_Site.bookings.helper_functions import generate_receipt_pdf

import json
from datetime import datetime, date
from sqlalchemy import func
from pathlib import Path

bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)


def make_booking_email_receipt_redirect(v: Viewing, seats_json, cash_payment_form=None, card_payment_form=None):
    seats = json.loads(seats_json)
    new_transaction, msg = v.book_seats(seats, current_user)
    if not new_transaction:
        flash(msg, 'danger')
        return render_book_specific_viewing(v, cash_payment_form=cash_payment_form, card_payment_form=card_payment_form)

    email_address = current_user.email
    if cash_payment_form:
        email_address = cash_payment_form.customer_email.data

    generate_receipt_pdf(new_transaction, email_address)

    return render_template('transaction_complete.html', transaction=new_transaction)


def get_validate_viewing(viewing_id):
    v = Viewing.query.get(viewing_id)
    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')

    # Check viewing in the future and not hidden
    if v.time < datetime.now() and not v.movie.hidden:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')
        return None

    return v


def render_book_specific_viewing(v: Viewing, cash_payment_form: CashPaymentForm = None,
                                 card_payment_form: CardPaymentForm = None):
    if not cash_payment_form:
        cash_payment_form = CashPaymentForm()
    if not card_payment_form:
        card_payment_form = CardPaymentForm()

    ticket_prices = {t.name.lower(): t.price for t in TicketType.query.all()}
    return render_template('select_time.html', title=v.movie.name, viewing=v, cash_payment_form=cash_payment_form,
                           card_payment_form=card_payment_form, ticket_prices=ticket_prices,
                           is_seat_available=v.is_seat_available)


@bookings_blueprint.route('/viewing/<int:viewing_id>', methods=['GET'])
@login_required
def view_specific(viewing_id):
    v = get_validate_viewing(viewing_id)
    if not v:
        return redirect(get_redirect_url())

    cash_payment_form = CashPaymentForm()
    return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)


@bookings_blueprint.route('/viewing/<int:viewing_id>/pay/cash', methods=['POST'])
@manager_permission.require(401)
def book_with_cash(viewing_id):
    v = get_validate_viewing(viewing_id)
    if not v:
        return redirect(get_redirect_url())

    cash_payment_form = CashPaymentForm()
    if not cash_payment_form.validate_on_submit():
        if cash_payment_form.seats_json.errors:
            flash(cash_payment_form.seats_json.errors[0], 'danger')
        return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)

    return make_booking_email_receipt_redirect(v, cash_payment_form.seats_json.data,
                                               cash_payment_form=cash_payment_form)


@bookings_blueprint.route('/viewing/<int:viewing_id>/pay/card', methods=['POST'])
@login_required
def book_with_card(viewing_id):
    v = get_validate_viewing(viewing_id)
    if not v:
        return redirect(get_redirect_url())

    card_payment_form = CardPaymentForm()
    if not card_payment_form.validate_on_submit():
        if card_payment_form.seats_json.errors:
            flash(card_payment_form.seats_json.errors[0], 'danger')
        return render_book_specific_viewing(v, card_payment_form=card_payment_form)

    # Process card payment

    if card_payment_form.remember:
        # Check card not already saved
        last_4_digits = card_payment_form.card.data[-4:]
        saved_card = SavedCard.query \
            .filter(SavedCard.user_id == current_user.id) \
            .filter(SavedCard.number.like(f'%{last_4_digits}')) \
            .first()

        if not saved_card:
            current_user.saved_cards.append(SavedCard(
                number=card_payment_form.card.data,
                expiry=card_payment_form.expiry.data
            ))
            db.session.commit()

    return make_booking_email_receipt_redirect(v, card_payment_form.seats_json.data,
                                               card_payment_form=card_payment_form)


@bookings_blueprint.route('/upcoming', methods=['GET'])
@login_required
def my_upcoming_bookings():
    transactions = Transaction.query \
        .join(Transaction.viewings) \
        .filter(func.date(Viewing.time) >= date.today()) \
        .filter(Transaction.user_id == current_user.id) \
        .order_by(func.date(Viewing.time)) \
        .all()

    return render_template('my_bookings.html', title='Upcoming bookings', transactions=transactions, show_all_btn=True)


@bookings_blueprint.route('/all', methods=['GET'])
@login_required
def my_bookings():
    transactions = Transaction.query \
        .join(Transaction.viewings) \
        .filter(Transaction.user_id == current_user.id) \
        .order_by(func.date(Viewing.time)) \
        .all()
    return render_template('my_bookings.html', title='All bookings', transactions=transactions)


@bookings_blueprint.route('/receipt/<int:transaction_id>', methods=['GET'])
@login_required
def view_receipt(transaction_id):
    t = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first()
    if not t:
        flash(f'Transaction with id \'{transaction_id}\' not found', 'danger')
        return redirect(get_redirect_url())

    path = t.get_receipt_path()
    if not Path(path).is_file():
        flash('Receipt not found', 'danger')
        return redirect(get_redirect_url())

    return send_file(path, attachment_filename='tickets.pdf')


@bookings_blueprint.route('/cancel/<int:transaction_id>', methods=['GET'])
@login_required
def cancel(transaction_id):
    t = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first()
    if not t:
        flash(f'Transaction with id \'{transaction_id}\' not found', 'danger')
        return redirect(get_redirect_url())

    db.session.delete(t)
    db.session.commit()

    return render_template('canceled_booking.html', title='Cancelled')
