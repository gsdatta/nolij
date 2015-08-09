from flask_script import Manager
from nolij.app import create_app
from nolij.auth.models import User
from nolij.database import db
import sys

app = create_app(__name__, 'dev')

manager = Manager(app)

@manager.command
def create_admin():
    """Creates the admin user."""
    comp = Company(name="nolij", domain="nolij.io")
    db.session.add(comp)
    db.session.commit()


    user = user_datastore.create_user(email='shit@nolij.io', password='asdf', name='Fucker', company_id=comp.id)
    db.session.add(user)
    db.session.commit()
