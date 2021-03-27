from Flask_Cinema_Site import db, models
from Flask_Cinema_Site.forms import SimpleForm
from Flask_Cinema_Site.movie.forms import NewMovieForm, EditMovieForm, SearchForm, SearchResultsForm
from Flask_Cinema_Site.models import Movie, Viewing
from Flask_Cinema_Site.helper_functions import save_picture, delete_picture, get_json_response
from Flask_Cinema_Site.roles import manager_permission

from flask import render_template, redirect, url_for, Blueprint, flash, request, abort, jsonify
from flask_api import status

from sqlalchemy import func, asc
from datetime import date, timedelta


movies_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates',
    static_folder='static'
)


@movies_blueprint.route('/', methods=['GET'])
def view_multiple():
    movies = Movie.query.filter_by(hidden=False).all()
    return render_template('view_multiple_movies.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/star', methods=['GET'])
def star_filter():
    movies = Movie.query.filter_by(hidden=False).all()
    return render_template('star_rating_filter.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/genre', methods=['GET'])
def genre_filter():
    movies = Movie.query.filter_by(hidden=False).all()
    return render_template('genre_filter.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/<int:movie_id>', methods=['GET'])
def view_specific(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        abort(404)

    # If hidden movie and not manager
    if m.hidden and not manager_permission.can():
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        abort(404)

    viewing_days = []
    for i in range(7):
        d = date.today() + timedelta(days=i)
        viewings = Viewing.query\
            .filter(Viewing.movie_id == movie_id)\
            .filter(func.date(Viewing.time) == d) \
            .order_by(asc(Viewing.time))\
            .all()
        viewing_days.append((d, viewings))

    return render_template('view_specific_movie.html', title=m.name, movie=m, viewing_days=viewing_days)


@movies_blueprint.route('/add', methods=['GET', 'POST'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def add():
    form = NewMovieForm()
    if request.method == 'GET':
        return render_template('add_movie.html', title='Add Movie', form=form)

    if not form.validate_on_submit():
        return render_template('add_movie.html', title='Add Movie', form=form), status.HTTP_400_BAD_REQUEST

    cover_art_filename = save_picture(form.picture.data, 'movie/static/cover_arts')

    m = Movie(
        name=form.name.data,
        overview=form.overview.data,
        released=form.released.data,
        duration=form.duration.data,
        rating=form.rating.data,
        directors=form.directors.data,
        cast=form.cast_list.data,
        genres=form.genres.data,
        cover_art_name=cover_art_filename,
        hidden=True
    )
    db.session.add(m)
    db.session.commit()

    flash(f'Movie \'{m.name}\' added successfully', 'success')
    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/<int:movie_id>/edit', methods=['GET', 'POST'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def edit(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id \'{movie_id}\' does not exist', 'danger')
        abort(404)

    form = EditMovieForm()
    if request.method == 'GET':
        form.init_with_movie(m)
        return render_template('edit_movie.html', title='Edit Movie', form=form, movie=m)

    if not form.validate_on_submit():
        return render_template('edit_movie.html', title='Edit Movie', form=form, movie=m), status.HTTP_400_BAD_REQUEST

    m.name = form.name.data
    m.overview = form.overview.data
    m.released = form.released.data
    m.rating = form.rating.data
    m.directors = form.directors.data
    m.cast = form.cast_list.data
    m.genres = form.genres.data

    db.session.commit()

    # Save picture / delete old one
    if form.picture.data:
        new_picture_name = save_picture(form.picture.data, 'movie', 'static', 'cover_arts')
        delete_picture('movie', 'static', 'cover_arts', m.cover_art_name)
        m.cover_art_name = new_picture_name

    flash(f'Movie \'{m.name}\' saved successfully', 'success')
    return redirect(url_for('movie.view_specific', movie_id=m.id))


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/hide', methods=['POST'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def hide():
    form = SimpleForm()
    if not form.validate_on_submit():
        return get_json_response('Error hide movie failed', status.HTTP_400_BAD_REQUEST)

    m = Movie.query.get(form.id.data)
    if not m:
        return get_json_response(f'Movie with id \'{form.id.data}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = True
    db.session.commit()

    return get_json_response(f'Movie with id \'{form.id.data}\' successfully hidden', status.HTTP_200_OK)


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/show', methods=['POST'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def show():
    form = SimpleForm()
    if not form.validate_on_submit():
        return get_json_response('Error show movie failed', status.HTTP_400_BAD_REQUEST)

    m = Movie.query.get(form.id.data)
    if not m:
        return get_json_response(f'Movie with id \'{form.id.data}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = False
    db.session.commit()

    return get_json_response(f'Movie with id \'{form.id.data}\' successfully unhidden', status.HTTP_200_OK)


@movies_blueprint.route('/delete', methods=['POST'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def delete():
    form = SimpleForm()
    if not form.validate_on_submit():
        return get_json_response('Delete movie failed', status.HTTP_400_BAD_REQUEST)

    m = Movie.query.get(form.id.data)
    if not m:
        return get_json_response(f'Movie with id \'{form.id.data}\' not found', status.HTTP_400_BAD_REQUEST)

    delete_picture('movie', 'static', 'cover_arts', m.cover_art_name)
    db.session.delete(m)
    db.session.commit()

    flash(f'Movie with id \'{form.id.data}\' successfully deleted', 'success')
    return get_json_response(f'Movie with id \'{form.id.data}\' successfully deleted', status.HTTP_200_OK)


@movies_blueprint.route('/manage', methods=['GET'])
@manager_permission.require(status.HTTP_401_UNAUTHORIZED)
def manage():
    movies = Movie.query.all()
    return render_template('manage_movie.html', title='Manage Movies', movies=movies)


@movies_blueprint.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if not form.validate_on_submit():
        return get_json_response('Search movie failed', status.HTTP_400_BAD_REQUEST)

    search_query = f'%{form.query.data}%'

    results = db.session.query(Movie.id, Movie.name).filter(
        Movie.name.like(search_query) | Movie.genres.like(search_query) | Movie.cast.like(search_query) |
        Movie.directors.like(search_query)) \
        .filter(~Movie.hidden) \
        .limit(5).all()

    movies = {m.name: m.id for m in results}
    return jsonify(movies)


@movies_blueprint.route('/search_results/')
def search_results():
    form = SearchResultsForm(request.args)
    if not form.validate_on_submit():
        pass

    search_query = f'%{form.query.data}%'

    results = db.session.query(Movie).filter(
        Movie.name.like(search_query) | Movie.genres.like(search_query) | Movie.cast.like(search_query) |
        Movie.directors.like(search_query)).filter(~Movie.hidden)\
        .all()

    return render_template('search_results.html', query=form.query.data, results=results)
