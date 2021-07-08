from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import date, timedelta


class SearchForm(FlaskForm):
    search_word = StringField('Строка для поиска: ', validators=[DataRequired()])
    date_before = DateField(format='%Y-%m-%d', default=date.today() - timedelta(1))
    date_after = DateField(format='%Y-%m-%d', default=date.today() - timedelta(1))
    save_db = BooleanField(label='Сохранить в БД')
    submit = SubmitField('Поиск')

