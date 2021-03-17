

from flask import render_template, redirect, url_for, Blueprint, flash, request, abort, jsonify

analysis_blueprint = Blueprint(
    'analysis', __name__,
    template_folder='templates'
)


@analysis_blueprint.route('/', methods=['GET'])
def view_multiple():
    return render_template('view_multiple_movies.html', title='Browse Movies')


@analysis_blueprint.route('/movie/<int:movie_id>', methods=['GET'])
def view_single_movie(movie_id):
    return render_template('view_single_movie.html', title='Browse Movies')
