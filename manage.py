from flask_script import Manager
from nolij.app import create_app
from nolij.auth.models import User, user_datastore
from nolij.company.models import Company
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

    user = user_datastore.create_user(email='admin@nolij.io', password='asdf', name='Admin', company_id=comp.id)
    db.session.add(user)
    db.session.commit()


@manager.command
def delete_db(new_admin=False):
    db.session.execute("DROP SCHEMA IF EXISTS public cascade;")
    db.session.execute("CREATE SCHEMA public;")
    db.session.remove()
    db.drop_all()
    db.create_all()

    if new_admin:
        create_admin()

if __name__ == "__main__":
    manager.run()
