from Flask_Cinema_Site import db
from Flask_Cinema_Site.forms import SimpleForm
from Flask_Cinema_Site.movie.forms import NewMovieForm, EditMovieForm
from Flask_Cinema_Site.models import Movie, Viewing
from Flask_Cinema_Site.helper_functions import get_redirect_url, save_picture, get_json_response

from flask import render_template, redirect, url_for, Blueprint, flash, request
from flask_api import status


movies_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates',
    static_folder='static'
)


@movies_blueprint.route('/', methods=['GET'])
def view_multiple():
    movies = Movie.query.filter_by(hidden=False).all()
    return render_template('view_multiple_movies.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/<int:movie_id>', methods=['GET'])
def view_specific(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        return redirect(get_redirect_url())

    viewings = Viewing.query.filter_by(movie_id=m.id).all()
    return render_template('view_specific_movie.html', title=m.name, movie=m, viewings=viewings)


@movies_blueprint.route('/add', methods=['GET'])
def add_get():
    # TODO Check user is manager

    form = NewMovieForm()
    return render_template('add_movie.html', title='Add Movie', form=form)


@movies_blueprint.route('/add', methods=['POST'])
def add_post():
    # TODO Check user is manager

    form = NewMovieForm()
    if not form.validate_on_submit():
        return render_template('add_movie.html', title='Add Movie', form=form)

    cover_art_filename = save_picture(form.picture.data, 'movie/static/cover_arts')

    m = Movie(
        name=form.name.data,
        overview=form.overview.data,
        released=form.released.data,
        rating=form.rating.data,
        directors=form.directors.data,
        cast=form.cast_list.data,
        genres=form.genres.data,
        cover_art_name=cover_art_filename
    )
    db.session.add(m)
    db.session.commit()

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit(movie_id):
    # TODO Check user is manager

    m = Movie.query.get(movie_id)

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

    if form.picture.data:
        # TODO delete picture
        m.cover_art_filename = save_picture(form.picture.data, 'movie/static/cover_arts')

    flash('Movie saved successfully', 'success')
    return redirect(url_for('movie.view_specific', movie_id=m.id))


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/hide', methods=['POST'])
def hide():
    # TODO Check user is manager

    form = SimpleForm()
    if not form.validate_on_submit():
        return get_json_response('Missing csrf token', status.HTTP_400_BAD_REQUEST)

    m = Movie.query.get(form.id)
    if not m:
        return get_json_response(f'Movie with id \'{form.id}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = True
    db.session.commit()

    return get_json_response(f'Movie with id \'{form.id}\' successfully hidden', status.HTTP_200_OK)


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/show', methods=['POST'])
def show():
    # TODO Check user is manager

    form = SimpleForm()
    if not form.validate_on_submit():
        return get_json_response('Missing csrf token', status.HTTP_400_BAD_REQUEST)

    m = Movie.query.get(form.id)
    if not m:
        return get_json_response(f'Movie with id \'{form.id}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = False
    db.session.commit()

    return get_json_response(f'Movie with id \'{form.id}\' successfully unhidden', status.HTTP_200_OK)


@movies_blueprint.route('/delete', methods=['POST'])
def delete():
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/manage', methods=['GET'])
def manage():
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))
