from nolij.database import db
from flask import current_app
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
import logging


# Association table for roles<->users
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    """
    This is to be used in the future when role based authentication is
    needed for superusers, etc. It is also needed by Flask-Security.
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    """
    This is the main User class and is the core of the auth module.
    It contains courses, token authentication, and roles.
    """

    id = db.Column(db.Integer, primary_key=True)

    # Initialize user metadata
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    company_id = db.Column(db.Integer(), db.ForeignKey('company.id'))
    company = db.relationship('Company')

    def as_dict(self):
        return {
                "id": self.id,
                "email": self.email,
                "courses": [course.as_dict() for course in self.courses],
                "university": self.university.as_dict()
                }


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
