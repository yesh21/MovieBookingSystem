from Flask_Cinema_Site.movie.forms import NewMovieForm

from flask import render_template, redirect, url_for, Blueprint

movies_blueprint = Blueprint(
    'movie', __name__,
    template_folder='templates'
)


@movies_blueprint.route('/', methods=['GET'])
def view_multiple():
    return render_template('view_multiple_movies.html')


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
