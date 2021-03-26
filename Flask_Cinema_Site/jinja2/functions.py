from flask import Markup


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
