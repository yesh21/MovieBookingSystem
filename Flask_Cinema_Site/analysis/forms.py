from flask_wtf import FlaskForm

from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError

from datetime import date, timedelta


class FilterForm(FlaskForm):
    class Meta:
        csrf = False
    start_date = DateField('Start date', validators=[])
    end_date = DateField('End date', validators=[])

    submit = SubmitField('Filter')

    def validate_start_date(self, start_date):
        # Default time period is one week
        if self.start_date.data is None and self.end_date.data is None:
            self.start_date.data = date.today() - timedelta(days=7)
            self.end_date.data = date.today()

        elif self.start_date.data is not None and self.end_date.data is None:
            self.end_date.data = self.start_date.data + timedelta(days=7)

        if self.start_date.data is None and self.end_date is not None:
            self.start_date.data = self.end_date.data - timedelta(days=7)

        if self.start_date.data > self.end_date.data:
            raise ValidationError('Start date must be before end date')
