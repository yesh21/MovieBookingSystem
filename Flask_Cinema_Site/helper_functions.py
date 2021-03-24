from Flask_Cinema_Site import app, mail

from flask import request, url_for, current_app, jsonify

from is_safe_url import is_safe_url
from PIL import Image, ImageOps
import os
import secrets

from flask_mail import Message
from threading import Thread


def get_redirect_url():
    # TODO ?next= dont work on POST requests???
    # TODO STOP redirect loops
    url = request.args.get('next')  # or request.referrer
    if url and is_safe_url(url, app.config['SAFE_URL_HOSTS']):
        return url
    return url_for('home.home')


def get_json_response(message, status_code):
    response = {
        'code': status_code,
        'msg': message
    }
    return jsonify(response), status_code


def save_picture(picture, *rel_folder_path):
    extension = os.path.splitext(picture.filename)[-1]
    name = secrets.token_hex(12) + extension
    path = os.path.join(current_app.root_path, *rel_folder_path, name)

    # output_size = (500, 500)
    pic = Image.open(picture)
    # Fix image orientation
    pic = ImageOps.exif_transpose(pic)

    # pic.thumbnail(output_size)
    pic.save(path)

    return name


def delete_picture(*rel_picture_path):
    path = os.path.join(current_app.root_path, *rel_picture_path)
    if not os.path.exists(path):
        return False

    os.remove(path)
    return True


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
