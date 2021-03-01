from flask import render_template, redirect, url_for, Blueprint, flash

from Flask_Cinema_Site import app, db, models, mail, helper_functions
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.models import Movie

bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)


# Will show movie, brief details and row of times for each day
# Once selected will redirect to seats
@bookings_blueprint.route('/<int:movie_id>', methods=['GET'])
def view_specific(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        return redirect(get_redirect_url())

    return render_template('select_time', title=m.name, movie=m)
