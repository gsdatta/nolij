from nolij.database import db
from sqlalchemy.sql import func
import datetime
import unicodedata
import re
from sqlalchemy.event import listens_for

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

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)


class Team(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    members = db.relationship("User", secondary=team_members)
    slug = db.Column(db.String(), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company")
    #main_wiki_id = db.Column(db.Integer(), db.ForeignKey("wiki.id"), nullable=True)
    #main_wiki = db.relationship("Wiki")

    administrators = db.relationship("User", secondary=team_administrators)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()


class Wiki(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"))
    team = db.relationship("Team")
    slug = db.Column(db.String(), nullable=False)

    description = db.Column(db.String(), nullable=True)

    administrators = db.relationship("User", secondary=wiki_administrators)

    main_wiki = db.Column(db.Boolean(), default=False, nullable=False)

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        success = False
        i = 2
        while not success:
            wiki = Wiki.query.filter_by(slug=self.slug).first()
            if wiki is None:
                success = True
            else:
                self.slug = self.slug + '-%s' % i
                i = i + 1

class Page(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    wiki_id = db.Column(db.Integer(), db.ForeignKey("wiki.id"))
    wiki = db.relationship("Wiki", backref=db.backref("pages"))
    name = db.Column(db.String(), nullable=False)
    text = db.Column(db.Text(), nullable=True)

    contributors = db.relationship("User", secondary=page_contribs)

    date_created = db.Column(db.DateTime(), default=func.now(), nullable=False)
    date_modified = db.Column(db.DateTime(), onupdate=datetime.datetime.now, nullable=False)


@listens_for(Wiki, 'before_insert')
def wiki_slug(mapper, connect, target):
    target.generate_slug()
