from nolij.database import db
from sqlalchemy.sql import func
import datetime
import unicodedata
import re
from sqlalchemy.event import listens_for

team_members = db.Table('team_members',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('studygroup_id', db.Integer(), db.ForeignKey('team.id')))

folio_administrators = db.Table('folio_adminstrators' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('folio_id', db.Integer(), db.ForeignKey('folio.id')))

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

class SlugMixin(object):
    slug = db.Column(db.String(), nullable=False)

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)
        success = False
        i = 2
        while not success:
            folio = Folio.query.filter_by(slug=self.slug).first()
            if folio is None:
                success = True
            else:
                self.slug = self.slug + '-%s' % i
                i = i + 1




class Team(db.Model):
    """
    A team provides the fundamental structure of a company. Each team is comprised of
    "teams". These teams can be anything generic such as 'Onboarding', or even
    'Engineering'. Each team contains its own folios and projects.
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    members = db.relationship("User", secondary=team_members)
    slug = db.Column(db.String(), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company")
    #main_folio_id = db.Column(db.Integer(), db.ForeignKey("folio.id"), nullable=True)
    #main_folio = db.relationship("Folio")

    administrators = db.relationship("User", secondary=team_administrators)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()


class Folio(SlugMixin, db.Model):
    """
    A folio contains the actual nolij within a team. A folio can have projects or
    pages tied to it.
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"))
    team = db.relationship("Team")
    slug = db.Column(db.String(), nullable=False)

    description = db.Column(db.String(), nullable=True)

    administrators = db.relationship("User", secondary=folio_administrators)



class Page(SlugMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    folio_id = db.Column(db.Integer(), db.ForeignKey("folio.id"), nullable=False)
    folio = db.relationship("Folio", backref=db.backref("pages"))


    name = db.Column(db.String(), nullable=False)
    text = db.Column(db.Text(), nullable=True)

    contributors = db.relationship("User", secondary=page_contribs)

    date_created = db.Column(db.DateTime(), default=func.now(), nullable=False)
    date_modified = db.Column(db.DateTime(), onupdate=func.now(), nullable=False, default=func.now())

    main_page = db.Column(db.Boolean(), default=False, nullable=False)

@listens_for(Folio, 'before_insert')
def folio_slug(mapper, connect, target):
    target.generate_slug()

@listens_for(Page, 'before_insert')
def page_slug(mapper, connect, target):
    target.generate_slug()
