from flask import render_template, redirect, Blueprint, flash, url_for
from flask_login import current_user, login_required

from Flask_Cinema_Site import db
from Flask_Cinema_Site.roles import manager_permission
from Flask_Cinema_Site.models import Movie, Viewing, User, Transaction, Seat, TicketType
from Flask_Cinema_Site.helper_functions import get_redirect_url, send_email
from Flask_Cinema_Site.bookings.forms import CardPaymentForm, CashPaymentForm
from Flask_Cinema_Site.bookings.helper_functions import create_pdf

import json
from datetime import datetime, date
from sqlalchemy import func

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
    
    # TODO email receipt

    # TODO Redirect to transaction successful page
    return redirect(url_for('movie.view_multiple'))


def get_validate_viewing(viewing_id):
    v = Viewing.query.get(viewing_id)
    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')

    # Check viewing in the future and not hidden
    if v.time < datetime.now() and not v.movie.hidden:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')

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
@manager_permission.require()
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

    # Simulate card checking
    return make_booking_email_receipt_redirect(v, card_payment_form.seats_json.data,
                                               card_payment_form=card_payment_form)


@bookings_blueprint.route('/upcoming', methods=['GET'])
@login_required
def my_upcoming_bookings():
    transactions = Transaction.query \
        .join(Transaction.viewings) \
        .filter(func.date(Viewing.time) >= date.today()) \
        .order_by(func.date(Viewing.time))\
        .group_by(Viewing.id) \
        .all()
    return render_template('my_bookings.html', title='Upcoming bookings', transactions=transactions, show_all_btn=True)


@bookings_blueprint.route('/all', methods=['GET'])
@login_required
def my_bookings():
    transactions = Transaction.query \
        .join(Transaction.viewings) \
        .order_by(func.date(Viewing.time))\
        .group_by(Viewing.id) \
        .all()
    return render_template('my_bookings.html', title='All bookings', transactions=transactions)


@bookings_blueprint.route("/pay", methods=['GET', 'POST'])
def payment():
    v = None
    m = None
    seats = None

    payment_form = CardPaymentForm()
    if payment_form.validate_on_submit():
        for seat in seats:
            double_booking = User.query.join(Transaction) \
                .filter(User.id == Transaction.user_id).join(Seat) \
                .filter(Transaction.id == Seat.transaction_id) \
                .filter(Seat.seat_number == seat).join(Viewing) \
                .filter(Seat.viewing_id == Viewing.id).first()
            # .filter(Viewing.time == v.time).first() PROBLEM WHEN ADDING TIME COMPARISON

            if double_booking:
                flash("Double booking detected!")
                return redirect(get_redirect_url())
        movie = Movie.query.filter(Movie.name == m.name).first()
        viewing = Viewing.query.filter(Viewing.movie_id == movie.id).first()
        current_date = datetime.now()

        transaction = Transaction(user_id=current_user.id, datetime=current_date)
        transaction.viewings.append(viewing)
        for seat in seats:
            seating = Seat.query.filter(seat == Seat.seat_number).first()
            transaction.seats.append(seating)
        db.session.add(transaction)
        db.session.commit()

        create_pdf(transaction.id, current_user.id, movie)
        flash("Thank you for booking with us, confirmation email will arrive soon!")
        return redirect(get_redirect_url())

    return render_template('payment.html', seats=seats, title=m.name, times=v, form=payment_form)
