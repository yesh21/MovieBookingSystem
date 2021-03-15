from flask import render_template, redirect, Blueprint, flash, request

from Flask_Cinema_Site.bookings.forms import PaymentForm
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.models import Movie, Viewing
import json

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


@bookings_blueprint.route("/pay", methods=['GET'])
def payment():
    # Final Transaction
    payment_form = PaymentForm()
    return render_template('payment.html', seats=seats, title=m.name, times=v, form=payment_form)
