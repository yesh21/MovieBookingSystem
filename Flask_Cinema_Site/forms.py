from flask_wtf import FlaskForm

from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange


# Simple form for requests that only require id / CSRF token
class SimpleForm(FlaskForm):
    id = IntegerField('', validators=[DataRequired(), NumberRange(min=0)])
