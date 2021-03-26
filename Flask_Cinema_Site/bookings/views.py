from flask import render_template, redirect, Blueprint, flash, request
from flask_login import current_user

from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, Viewing, User, Transaction, Seat, TicketType
from Flask_Cinema_Site.helper_functions import get_redirect_url, send_email
from Flask_Cinema_Site.bookings.forms import PaymentForm, CashPaymentForm
from Flask_Cinema_Site.bookings.helper_functions import create_pdf

import json
from datetime import datetime

bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)


def render_book_specific_viewing(v: Viewing, cash_payment_form: CashPaymentForm = None):
    if not cash_payment_form:
        cash_payment_form = CashPaymentForm()

    ticket_prices = {t.name.lower(): t.price for t in TicketType.query.all()}
    return render_template('select_time.html', title=v.movie.name, viewing=v, cash_payment_form=cash_payment_form,
                           ticket_prices=ticket_prices, is_seat_available=v.is_seat_available)


# Will show movie, brief details and row of times for each day
# Once selected will redirect to seats
@bookings_blueprint.route('/viewing/<int:viewing_id>', methods=['GET'])
def view_specific(viewing_id):
    v = Viewing.query.get(viewing_id)
    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')
        return redirect(get_redirect_url())

    # Check viewing in the future

    cash_payment_form = CashPaymentForm()
    return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)


@bookings_blueprint.route('/viewing/<int:viewing_id>/pay/cash', methods=['POST'])
def book_with_cash(viewing_id):
    v = Viewing.query.get(viewing_id)
    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')
        return redirect(get_redirect_url())

    # Check viewing in the future

    cash_payment_form = CashPaymentForm()
    if not cash_payment_form.validate_on_submit():
        if cash_payment_form.seats_json.errors:
            flash(cash_payment_form.seats_json.errors[0], 'danger')
        return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)

    seats = json.loads(cash_payment_form.seats_json.data)
    new_transaction, msg = v.book_seats(seats, current_user)
    if not new_transaction:
        flash(msg, 'danger')
        return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)

    # Redirect to transaction successful page
    return render_book_specific_viewing(v, cash_payment_form=cash_payment_form)


@bookings_blueprint.route("/pay", methods=['GET', 'POST'])
def payment():
    v = None
    m = None
    seats = None

    payment_form = PaymentForm()
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
