from flask import Blueprint, redirect, url_for

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


@home_blueprint.route('/', methods=['GET'])
def home():
    return redirect(url_for('movie.view_multiple'))
