from Flask_Cinema_Site.models import Movie

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange


class NewMovieForm(FlaskForm):
    name = StringField('Name *', validators=[DataRequired(), Length(min=5, max=100)])
    overview = TextAreaField('Overview *', validators=[DataRequired(), Length(min=5, max=500)])

    released = DateField('Released *', validators=[DataRequired()])

    picture = FileField('Upload cover art *', validators=[DataRequired(message='Cover art is required.'),
                                                          FileAllowed(['jpg', 'jpeg', 'png'])])

    duration = IntegerField('Duration *', validators=[DataRequired()])
    rating = DecimalField('Rating *',
                          validators=[DataRequired(), NumberRange(message='Ratings must be between 1 and 5 stars',
                                                                  min=1, max=5,)])

    directors = TextAreaField('Directors', validators=[Length(min=0, max=250)])
    cast_list = TextAreaField('Cast list', validators=[Length(min=0, max=250)])
    genres = TextAreaField('Genres', validators=[Length(min=0, max=250)])

    submit = SubmitField('Add')


class EditMovieForm(NewMovieForm):
    picture = FileField('Upload cover art', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Save')

    def init_with_movie(self, m: Movie):
        self.name.data = m.name
        self.overview.data = m.overview
        self.released.data = m.released
        self.duration.data = m.duration
        self.rating.data = m.rating
        self.directors.data = m.directors
        self.cast_list.data = m.cast
        self.genres.data = m.genres
