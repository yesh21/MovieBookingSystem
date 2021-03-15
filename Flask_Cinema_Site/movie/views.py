from Flask_Cinema_Site import db, models
from Flask_Cinema_Site.forms import SimpleForm
from Flask_Cinema_Site.movie.forms import NewMovieForm, EditMovieForm
from Flask_Cinema_Site.models import Movie, Viewing
from Flask_Cinema_Site.helper_functions import save_picture, delete_picture, get_json_response

from flask import render_template, redirect, url_for, Blueprint, flash, request, abort, jsonify
from flask_api import status
from flask_cors import cross_origin

import sqlite3 as sql
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


@movies_blueprint.route('/<int:movie_id>', methods=['GET'])
def view_specific(movie_id):
    m = Movie.query.get(movie_id)
    if not m:
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
def add():
    # TODO Check user is manager

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
def edit(movie_id):
    # TODO Check user is manager

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
def hide():
    # TODO Check user is manager

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
def show():
    # TODO Check user is manager

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
def delete():
    # TODO Check user is manager

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
def manage():
    # TODO Check user is manager

    movies = Movie.query.all()
    return render_template('manage_movie.html', title='Manage Movies', movies=movies)


@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
@movies_blueprint.route('/search', methods=['POST'])
def search():
    if request.method == 'POST' and request.form.get("search_button") == 'search_results':
        search = request.form.get("search")
        return redirect(url_for('movie.search_results', query=search))
    con = sql.connect("site.db")
    cur = con.cursor()
    term = request.form['q']
    print('term: ', term)
    cur.execute("SELECT name FROM movie WHERE name LIKE ?""", ('%' + term + '%', ))
    con.commit()
    rows = {}
    rows = cur.fetchmany(5)
    my_list = []
    for i in range(len(rows)):
        my_list.append(rows[i][0])
    if len(my_list) == 0:
        my_list.append("No results found-" + term)
        rows += db.session.query(models.Movie.name).order_by(models.Movie.released.desc()).limit(2).all()
        for i in range(len(rows)):
            my_list.append(rows[i][0] + '(suggestion)')
    return jsonify(my_list)


@movies_blueprint.route('/search_results/<query>')
def search_results(query):
    noresults = False
    search = "%{}%".format(query)
    results1 = db.session.query(models.Movie).filter(models.Movie.name.like(search)).all()
    results2 = db.session.query(models.Movie).filter(models.Movie.genres.like(search)).all()
    results3 = db.session.query(models.Movie).filter(models.Movie.cast.like(search)).all()
    results4 = db.session.query(models.Movie).filter(models.Movie.directors.like(search)).all()
    results = results1 + results2 + results3 + results4
    results = set(results)
    if len(results) == 0:
        noresults = True
        results = db.session.query(models.Movie).order_by(models.Movie.released.desc()).limit(2).all()
    return render_template('search_results.html',
                           query=query,
                           results=results, noresults=noresults)
