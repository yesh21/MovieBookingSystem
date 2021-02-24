from Flask_Cinema_Site.movie.forms import NewMovieForm
from Flask_Cinema_Site.models import Movie
from Flask_Cinema_Site.helper_functions import get_redirect_url

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
def add():
    form = NewMovieForm()
    return render_template('add_movie.html', title='Add Movie', form=form)


@movies_blueprint.route('/<int:movie_id>/edit', methods=['GET'])
def edit(movie_id):
    return render_template('edit_movie.html')


@movies_blueprint.route('/delete', methods=['POST'])
def delete(film_id):
    return redirect(url_for('view_multiple'))
