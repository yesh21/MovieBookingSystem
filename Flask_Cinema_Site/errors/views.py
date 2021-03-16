from Flask_Cinema_Site import app

from flask import render_template
from flask_api import status


@app.errorhandler(status.HTTP_401_UNAUTHORIZED)
def unauthorized(e):
    return render_template('errors/401.html'), status.HTTP_401_UNAUTHORIZED


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(e):
    return render_template('errors/404.html'), status.HTTP_404_NOT_FOUND
