from Flask_Cinema_Site import app

from flask import request, url_for

from is_safe_url import is_safe_url


def get_redirect_url():
    url = request.args.get('next') or request.referrer
    if url and is_safe_url(url, app.config['SAFE_URL_HOSTS']):
        return url
    return url_for('home')
