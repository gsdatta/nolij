from flask_security.forms import RegisterForm
from nolij.auth.models import User
from wtforms.fields import TextField, StringField, PasswordField
from wtforms import validators
from flask_wtf import Form

class UserRegistrationForm(Form):
    name = StringField('Full Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Please enter the same password!')])
    confirm = PasswordField('Repeat Password')
    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise validators.ValidationError('A user with this email already exists')