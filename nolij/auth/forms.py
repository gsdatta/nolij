from flask_security.forms import RegisterForm
from wtforms.fields import TextField
from wtforms.validators import Required

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Company Name', [Required()])
    domain = TextField('Company Domain', [Required()])

