from Flask_Cinema_Site import db
from Flask_Cinema_Site.models import Movie, TicketType, Seat, Viewing
from Flask_Cinema_Site.roles import manager_permission
from Flask_Cinema_Site.helper_functions import get_redirect_url
from Flask_Cinema_Site.analysis.forms import FilterForm

from flask import render_template, redirect, Blueprint, flash, request
from flask_api import status

from sqlalchemy import func, distinct
from datetime import date, timedelta

analysis_blueprint = Blueprint(
    'analysis', __name__,
    template_folder='templates'
)


@analysis_blueprint.route('/', methods=['GET'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def view_multiple():
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()

    form = FilterForm(request.args)
    if form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data

    totals = db.session.query(
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue')) \
        .join(Viewing.seats) \
        .join(Seat.ticket_type) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .first()

    totals_by_ticket_type = db.session.query(
        TicketType.name,
        func.count(Seat.id).label('seats_sold'),
        func.sum(TicketType.price).label('revenue'))\
        .join(TicketType.seats)\
        .join(Seat.viewing)\
        .filter(func.date(Viewing.time) >= start_date)\
        .filter(func.date(Viewing.time) <= end_date)\
        .group_by(TicketType.id)\
        .all()

    totals_by_movie = db.session.query(
        Movie.id,
        Movie.name,
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue'))\
        .join(Movie.viewings)\
        .join(Viewing.seats)\
        .join(Seat.ticket_type) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .group_by(Movie.id)\
        .all()

    totals_by_date = db.session.query(
        Viewing.time.label('date'),
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue'))\
        .join(Viewing.seats)\
        .join(Seat.ticket_type) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .group_by(func.date(Viewing.time))\
        .all()

    return render_template('view_totals.html', title='Analysis - All', form=form,
                           start_date=start_date, end_date=end_date,
                           totals=totals,
                           totals_by_date=totals_by_date,
                           totals_by_ticket_type=totals_by_ticket_type,
                           totals_by_movie=totals_by_movie)


@analysis_blueprint.route('/movie/<int:movie_id>', methods=['GET'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def view_single_movie(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id \'{movie_id}\' not found', 'danger')
        return redirect(get_redirect_url())

    start_date = date.today() - timedelta(days=7)
    end_date = date.today()

    form = FilterForm(request.args)
    if form.validate():
        start_date = form.start_date.data
        end_date = form.end_date.data

    totals = db.session.query(
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue')) \
        .join(Viewing.seats) \
        .join(Seat.ticket_type) \
        .filter(Viewing.movie_id == m.id) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .first()

    totals_by_ticket_type = db.session.query(
        TicketType.name,
        func.count(Seat.id).label('seats_sold'),
        func.sum(TicketType.price).label('revenue')) \
        .join(TicketType.seats) \
        .join(Seat.viewing) \
        .filter(Viewing.movie_id == m.id) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .group_by(TicketType.id) \
        .all()

    totals_by_viewing = db.session.query(
        Viewing.id,
        Viewing.time,
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue')) \
        .join(Viewing.seats) \
        .join(Seat.ticket_type) \
        .filter(Viewing.movie_id == m.id) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .group_by(Viewing.id) \
        .all()

    totals_by_date = db.session.query(
        Viewing.time.label('date'),
        func.count(Seat.id).label('seats_sold'),
        func.count(distinct(Seat.transaction_id)).label('num_transactions'),
        func.sum(TicketType.price).label('revenue')) \
        .join(Viewing.seats) \
        .join(Seat.ticket_type) \
        .filter(Viewing.movie_id == m.id) \
        .filter(func.date(Viewing.time) >= start_date) \
        .filter(func.date(Viewing.time) <= end_date) \
        .group_by(func.date(Viewing.time)) \
        .all()

    return render_template('view_totals.html', title=f'Analysis - {m.name}', form=form,
                           start_date=start_date, end_date=end_date,
                           totals=totals,
                           totals_by_date=totals_by_date,
                           totals_by_ticket_type=totals_by_ticket_type,
                           totals_by_viewing=totals_by_viewing)
