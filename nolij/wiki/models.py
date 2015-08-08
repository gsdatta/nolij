from nolij.database import db
from sqlalchemy.sql import func
import datetime

team_members = db.Table('team_members',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('studygroup_id', db.Integer(), db.ForeignKey('team.id')))

wiki_administrators = db.Table('wiki_adminstrators' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('wiki_id', db.Integer(), db.ForeignKey('wiki.id')))

team_administrators = db.Table('team_administrators' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('team_id', db.Integer(), db.ForeignKey('team.id')))

page_contribs = db.Table('page_contribs' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('page_id', db.Integer(), db.ForeignKey('page.id')))

class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    members = db.relationship("User", secondary=team_members)

    #main_wiki_id = db.Column(db.Integer(), db.ForeignKey("wiki.id"), nullable=True)
    #main_wiki = db.relationship("Wiki")

    administrators = db.relationship("User", secondary=team_administrators)


class Wiki(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"))
    team = db.relationship("Team")

    description = db.Column(db.String(), nullable=True)

    administrators = db.relationship("User", secondary=wiki_administrators)

    main_wiki = db.Column(db.Boolean(), default=False, nullable=False)

class Page(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    wiki_id = db.Column(db.Integer(), db.ForeignKey("wiki.id"))
    wiki = db.relationship("Wiki")

    text = db.Column(db.Text(), nullable=True)

    contributors = db.relationship("User", secondary=page_contribs)

    date_created = db.Column(db.DateTime(), default=func.now(), nullable=False)
    date_modified = db.Column(db.DateTime(), onupdate=datetime.datetime.now, nullable=False)
