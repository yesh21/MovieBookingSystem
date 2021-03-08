from Flask_Cinema_Site import db, models
from Flask_Cinema_Site.movie.forms import NewMovieForm
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
        directors=form.directors.data,
        duration=form.duration.data,
        rating=form.rating.data,
        hidden=0,
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


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/<int:movie_id>/hide', methods=['POST'])
def hide(movie_id):
    # TODO Check user is manager

    m = Movie.query.get(movie_id)
    if not m:
        return get_json_response(f'Movie with id \'{movie_id}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = True
    db.session.commit()

    return get_json_response(f'Movie with id \'{movie_id}\' successfully hidden', status.HTTP_200_OK)


# Probably should use flak-api or flask-restful idk?
@movies_blueprint.route('/<int:movie_id>/show', methods=['POST'])
def show(movie_id):
    # TODO Check user is manager

    m = Movie.query.get(movie_id)
    if not m:
        return get_json_response(f'Movie with id \'{movie_id}\' not found', status.HTTP_400_BAD_REQUEST)

    m.hidden = False
    db.session.commit()

    return get_json_response(f'Movie with id \'{movie_id}\' successfully unhidden', status.HTTP_200_OK)


@movies_blueprint.route('/delete', methods=['POST'])
def delete():
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/manage', methods=['GET'])
def manage():
    # TODO Check user is manager

    return redirect(url_for('movie.view_multiple'))


@movies_blueprint.route('/search', methods=['POST'])
def search():
    search = request.form.get("search")
    return redirect(url_for('movie.search_results', query=search))


@movies_blueprint.route('/search_results/<query>')
def search_results(query):
    message = ""
    results1 = db.session.query(models.Movie).filter(models.Movie.name.ilike(query)).all()
    results2 = db.session.query(models.Movie).filter(models.Movie.cover_art_name.ilike(query)).all()
    results3 = db.session.query(models.Movie).filter(models.Movie.released.ilike(query)).all()
    results = results1 + results2 + results3
    # results = set(results)
    if len(results) == 0:
        message += "No results found"
    return "Done"
