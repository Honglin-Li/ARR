from wtforms.form import Form
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.utils.const import MONTHS
from datetime import datetime


class ReviewSearchForm(Form):
    search_text = StringField('input reviewer name',
                              validators=[DataRequired(message='Please input reviewer name'),
                                          Length(1, 100, message='max length:100')])
    submit = SubmitField('search reviewers')


class YearMonthFilterForm(Form):
    # create items for select input fields
    month_items = [(k, v) for k, v in MONTHS.items()]

    start_year = 2021
    end_year = datetime.today().year
    year_items = [(year, year) for year in range(end_year, start_year-1, -1)]

    year = SelectField('Year',
                       choices=year_items,
                       validators=[DataRequired(message='Please input year')])
    month = SelectField('Month',
                        choices=month_items,
                        validators=[DataRequired(message='Please input month')])
    submit = SubmitField('Apply')