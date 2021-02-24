from Flask_Cinema_Site.movie.forms import NewMovieForm
from Flask_Cinema_Site.models import Movie

from flask import render_template, redirect, url_for, Blueprint

from datetime  import date

movies_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates'
)


@movies_blueprint.route('/', methods=['GET'])
def view_multiple():
    m = Movie()
    m.name = 'Black Widow'
    m.overview = 'In Marvel Studios’ action-packed spy thriller “Black Widow,” Natasha Romanoff aka Black Widow confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises. Pursued by a force that will stop at nothing to bring her down, Natasha must deal with her history as a spy and the broken relationships left in her wake long before she became an Avenger.'
    m.released = date(2021, 5, 7)
    m.cover_art_name = 'black_widow.jpg'
    m.directors = 'Cate Shortland'
    m.cast = 'Rachel Weisz, David Harbour, O-T Fagbenle, Ray Winstone, Florence Pugh, Scarlett Johansson'

    movies = [
        'm'
    ]
    return render_template('view_multiple_movies.html', title='Browse Movies', movies=movies)


@movies_blueprint.route('/<int:film_id>', methods=['GET'])
def view_specific(film_id):
    return render_template('view_specific_movie.html')


@movies_blueprint.route('/add', methods=['GET'])
def add():
    form = NewMovieForm()
    return render_template('add_movie.html', title='Add Movie', form=form)


@movies_blueprint.route('/<int:film_id>/edit', methods=['GET'])
def edit(film_id):
    return render_template('edit_movie.html')


@movies_blueprint.route('/delete', methods=['POST'])
def delete(film_id):
    return redirect(url_for('view_multiple'))
