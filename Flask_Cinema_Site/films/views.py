from flask import render_template, redirect, url_for, Blueprint


films_blueprint = Blueprint(
    'films', __name__,
    template_folder='templates'
)


@films_blueprint.route('/', methods=['GET'])
def view_multiple():
    return render_template('view_multiple_films.html')


@films_blueprint.route('/<int:film_id>', methods=['GET'])
def view_specific(film_id):
    return render_template('view_specific_film.html')


@films_blueprint.route('/add', methods=['GET'])
def add():
    return render_template('add_film.html')


@films_blueprint.route('/<int:film_id>/edit', methods=['GET'])
def edit(film_id):
    return render_template('edit_film.html')


@films_blueprint.route('/delete', methods=['POST'])
def edit(film_id):
    return redirect(url_for('view_multiple'))
