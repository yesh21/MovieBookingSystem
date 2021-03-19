from flask import render_template, redirect, Blueprint, flash, request
from flask_login import current_user

from Flask_Cinema_Site.bookings.forms import PaymentForm
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.models import Movie, Viewing, User, Transaction, Seat
from Flask_Cinema_Site import db

import json
from datetime import datetime

bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)

# Global Variables to keep track of current booking
# Probably a better way to do this
seats = None
m = None
v = None


# Will show movie, brief details and row of times for each day
# Once selected will redirect to seats
@bookings_blueprint.route('/slot', methods=['GET'])
def view_specific():
    movie_id = request.args.get('movie', None)
    viewing_id = request.args.get('viewing', None)

    global m, v

    m = Movie.query.get(movie_id)
    v = Viewing.query.get(viewing_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        return redirect(get_redirect_url())

    if not v:
        flash(f'Viewing with id [{viewing_id}] not found', 'danger')
        return redirect(get_redirect_url())

    # viewings = Viewing.query.filter_by(movie_id=m.id).all()
    return render_template('select_time.html', title=m.name, movie=m, times=v)


# Stores currently selected seats.
@bookings_blueprint.route("/slot/seats", methods=['POST'])
def seat_book():
    global seats
    seats = json.loads(request.data)

    # Add seats to the database

    return json.dumps({'status': 'OK'})


@bookings_blueprint.route("/pay", methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm()
    if payment_form.validate_on_submit():
        for seat in seats:
            double_booking = User.query.join(Transaction).join(Seat)\
                            .filter(Transaction.id == Seat.transaction_id)\
                            .filter(Seat.seat_number == seat).all()
            print(double_booking)
            if double_booking:
                flash("Double booking detected!")
                return redirect(get_redirect_url())
        movie = Movie.query.filter(Movie.name == m.name).first()
        viewing = Viewing.query.filter(Viewing.movie_id == movie.id).first()
        current_date = datetime.now()

        transaction = Transaction(user_id = current_user.id, datetime = current_date)
        transaction.viewings.append(viewing)
        for seat in seats:
            seating = Seat.query.filter(seat == Seat.seat_number).first()
            transaction.seats.append(seating)
        db.session.add(transaction)
        db.session.commit()

        send_ticket()
        flash("Thank you for booking with us, confirmation email will arrive soon!")
        return redirect(get_redirect_url())

    return render_template('payment.html', seats=seats, title=m.name, times=v, form=payment_form)

# Confirmation Email sent from this function
def send_ticket():
    # Ticket confirmation sent here

    return None
