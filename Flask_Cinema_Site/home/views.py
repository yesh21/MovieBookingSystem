from flask import Blueprint, redirect, url_for, render_template
from Flask_Cinema_Site import app, Movie

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates',
    static_folder='static'
)

@app.route('/', methods=['GET'])
def boot():
    return redirect(url_for('home.home'))

@home_blueprint.route('/', methods=['GET'])
def home():
    movies = Movie.query.filter_by(hidden=False).all()
    movies = movies[:4]
    return render_template('home_base.html', movies=movies)
    #return redirect(url_for('movie.view_multiple'))
