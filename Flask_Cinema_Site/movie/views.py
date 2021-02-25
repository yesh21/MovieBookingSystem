from Flask_Cinema_Site import db
from Flask_Cinema_Site.movie.forms import NewMovieForm
from Flask_Cinema_Site.models import Movie
from Flask_Cinema_Site.helper_functions import get_redirect_url, save_picture

from flask import render_template, redirect, url_for, Blueprint, flash

from datetime import date

movies_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates',
    static_folder='static'
)


@movies_blueprint.route('/', methods=['GET'])
def view_multiple():
    movies = Movie.query.all()
    return render_template('view_multiple_movies.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/<int:movie_id>', methods=['GET'])
def view_specific(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
        flash(f'Movie with id [{movie_id}] not found', 'danger')
        return redirect(get_redirect_url())

    return render_template('view_specific_movie.html', title=m.name, movie=m)


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
        directors=form.directors.data,
        cast=form.cast_list.data,
        genres=form.genres.data,
        cover_art_name=cover_art_filename
    )
    db.session.add(m)
    db.session.commit()

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/<int:movie_id>/edit', methods=['GET'])
def edit_get(movie_id):
    # TODO Check user is manager

    return render_template('edit_movie.html')


@movies_blueprint.route('/<int:movie_id>/edit', methods=['POST'])
def edit_post(movie_id):
    # TODO Check user is manager

    return render_template('edit_movie.html')


@movies_blueprint.route('/delete', methods=['POST'])
def delete(film_id):
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/manage', methods=['GET'])
def manage():
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))
