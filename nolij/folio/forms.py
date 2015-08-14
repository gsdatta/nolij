from wtforms.fields import StringField, TextField, BooleanField
from wtforms import validators
from flask_wtf import Form


class TeamForm(Form):
    name = StringField('Team Name', validators=[validators.input_required()])
    private = BooleanField('Private', validators=[])


class SearchForm(Form):
    query = StringField('Search', validators=[validators.input_required()], description='Search')
