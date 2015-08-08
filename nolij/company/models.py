from nolij.database import db

class Company(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    domain = db.Column(db.String(), nullable=False)
