from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class NewMovieForm(FlaskForm):
    name = StringField('Name *', validators=[DataRequired(), Length(min=5, max=100)])
    overview = TextAreaField('Overview *', validators=[DataRequired(), Length(min=5, max=250)])

    released = DateField('Released', validators=[DataRequired()])

    picture = FileField('Upload cover art *',
                        validators=[DataRequired(message='Product picture is required'),
                                    FileAllowed(['jpg', 'jpeg', 'png'])])

    directors = TextAreaField('Directors', validators=[Length(min=0, max=250)])
    cast_list = TextAreaField('Cast list', validators=[Length(min=0, max=250)])

    add_btn = SubmitField('Add')
