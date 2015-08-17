from wtforms.fields import StringField, TextField
from wtforms import validators
from flask_wtf import Form
from nolij.company.models import Company

class CompanyForm(Form):
    name = StringField('Company Name', validators=[validators.input_required()])
    domain = StringField('Company Domain', validators=[validators.input_required()])

    def validate_domain(form, field):
        company = Company.query.filter_by(domain=field.data).first()
        if company is not None:
            raise validators.ValidationError('A company with this domain already exists.')
