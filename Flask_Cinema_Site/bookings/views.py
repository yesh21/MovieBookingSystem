from flask import render_template, redirect, url_for, Blueprint, flash, request

from Flask_Cinema_Site import app, db, models, mail, helper_functions
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.models import Movie, Viewing

bookings_blueprint = Blueprint(
    'bookings', __name__,
    template_folder='templates',
    static_folder='static'
)


# Will show movie, brief details and row of times for each day
# Once selected will redirect to seats
@bookings_blueprint.route('/slot', methods=['GET'])
def view_specific():
    movie_id = request.args.get('movie', None)
    viewing_id = request.args.get('viewing', None)

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
