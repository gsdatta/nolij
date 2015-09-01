from flask_security.forms import RegisterForm
from nolij.auth.models import User
from nolij.company.models import Company 
from wtforms.fields import TextField, StringField, PasswordField
from wtforms import validators
from flask_wtf import Form

class CompanyRegistrationForm(Form):
    name = StringField('Full Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')

    def validate_comapny(form,field): 
        company = Company.query.filter_by(name = field.data).second() 
        if company is not None: 
            raise validators.ValidationError('This company already exists.')

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise validators.ValidationError('A user with this email already exists.')
    #def validate_token(field):
