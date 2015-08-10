from wtforms.fields import StringField, TextField, BooleanField
from wtforms import validators
from flask_wtf import Form
from nolij.folio.models import Team

class TeamForm(Form):
    name = StringField('Team Name', validators=[validators.input_required()])
    private = BooleanField('Private', validators=[validators.input_required()])
