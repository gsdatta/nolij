from wtforms.fields import StringField, TextField, BooleanField, TextAreaField
from wtforms import validators
from flask_wtf import Form


class TeamForm(Form):
    name = StringField('Team Name', validators=[validators.input_required()])
    members = TextAreaField('Members', validators=[], description='Enter member emails here, separated by new lines.')
    private = BooleanField('Private', validators=[])


class SearchForm(Form):
    query = StringField('Search', validators=[validators.input_required()], description='Search')
