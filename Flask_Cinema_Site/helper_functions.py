from Flask_Cinema_Site import app

from flask import request, url_for, current_app

from is_safe_url import is_safe_url
from PIL import Image, ImageOps
import os
import secrets


def get_redirect_url():
    url = request.args.get('next') or request.referrer
    if url and is_safe_url(url, app.config['SAFE_URL_HOSTS']):
        return url
    return url_for('home')


def save_picture(picture, rel_folder_path):
    extension = os.path.splitext(picture.filename)[-1]
    name = secrets.token_hex(12) + extension
    path = os.path.join(current_app.root_path, rel_folder_path, name)

    # output_size = (500, 500)
    pic = Image.open(picture)
    # Fix image orientation
    pic = ImageOps.exif_transpose(pic)

    # pic.thumbnail(output_size)
    pic.save(path)

    return name
