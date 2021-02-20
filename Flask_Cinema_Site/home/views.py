from flask import render_template, Blueprint
from Flask_Cinema_Site import app
from Flask_Cinema_Site import db,models


home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

