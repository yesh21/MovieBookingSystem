from Flask_Cinema_Site import app, mail

from flask import request, url_for, current_app, Markup, jsonify

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


def get_field_errors_html(errors):
    html = '<div class="invalid-feedback">'
    for err in errors:
        html += f'<p class="mb-0">{err}</p>'
    html += '</div>'
    return Markup(html)


def get_file_upload_errors_html(errors):
    html = '<div class="text-danger">'
    for err in errors:
        html += f'<small>{err}</small>'
    html += '</div>'
    return Markup(html)


def get_field_html(form_field, **kwargs):
    # Add label
    html = form_field.label(**{'class': 'form-control-label'})

    # Add field
    field_class = 'form-control is-invalid' if form_field.errors else 'form-control'
    field_dict = {**{'class': field_class}, **kwargs}
    html += form_field(**field_dict)

    # Field errors
    html += get_field_errors_html(form_field.errors)

    return html


def get_field_group_html(form_field, **kwargs):
    html = Markup('<div class="form-group">')
    html += get_field_html(form_field, **kwargs)
    html += Markup('</div>')
    return html


def get_file_upload_group_html(form_field, **kwargs):
    html = Markup('<div class="form-group">')
    # Add label
    html += form_field.label(**{'class': 'form-control-label'})

    # Add field
    field_dict = {**{'class': 'form-control-file'}, **kwargs}
    html += form_field(**field_dict)

    # Field errors
    html += get_file_upload_errors_html(form_field.errors)

    html += Markup('</div>')
    return html


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
