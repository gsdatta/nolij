from nolij.database importd db
from sqlalchemy.sql import func
import datetime
import unicodedata
import re
from sqlalchemy.event import listens_for
from flask_sqlalchemy import BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType

<<<<<<< HEAD
executive_board = db.table('executive_board',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('executive_permission', db.Integer(), db.ForeignKey('executive.id'))) 

=======
# Association table for team<->users (members)
>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
team_members = db.Table('team_members',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('team_id', db.Integer(), db.ForeignKey('team.id')))

# Association table for folio<->users (admins)
folio_administrators = db.Table('folio_adminstrators' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('folio_id', db.Integer(), db.ForeignKey('folio.id')))

# Association table for team<->users (admins)
team_administrators = db.Table('team_administrators' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('team_id', db.Integer(), db.ForeignKey('team.id')))

# Association table for page<->users (contributors)
page_contribs = db.Table('page_contribs' ,
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('page_id', db.Integer(), db.ForeignKey('page.id')))


# class TeamMembers(db.Model):
#     __tablename__ = 'team_members'
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True)
#
#     user = db.relationship("User")
#     team = db.relationship("")

def slugify(value):
<<<<<<< HEAD
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')          ##Hash
=======
    """
    Returns a slug given a string.

    :param value: The string to slugify
    :return: A slug (String)
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

class SlugMixin(object):

    """
    This mixin can be added to any model to provide slug functionality.

    However, a `before_install` event listener needs to be added
    as seen at the bottom of this file.
    """

    slug = db.Column(db.String(), nullable=False)

    def generate_slug(self, field):
        """
        Generates a slug for the object based on the given field.
        If an object with that slug exists, then add a number to the
        slug in the form slug-#, and increment the number until such
        a slug is found.
        """
        if not self.slug:
            self.slug = slugify(field)

        # If this slug is unique, go ahead and skip the loop
        success = self.query.filter_by(slug=self.slug).first() is None
        new_slug = self.slug

        # Loop continually until the correct slug has been found
        i = 2
        while not success:
            new_slug = self.slug + '-%s' % i
            # TODO: USE COUNT
            obj = self.query.filter_by(slug=new_slug).first()
            if obj is None:
                success = True
            else:
                i = i + 1

<<<<<<< HEAD
class Team(db.Model):
=======
        self.slug = new_slug


class Team(SlugMixin, db.Model):
>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
    """
    A team provides the fundamental structure of a company. Each team is comprised of
    "teams". These teams can be anything generic such as 'Onboarding', or even
    'Engineering'. Each team contains its own folios and projects.
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
<<<<<<< HEAD
    members = db.relationship("User", secondary=team_members)
    slug = db.Column(db.String(), nullable=False)
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company")

    #main_folio_id = db.Column(db.Integer(), db.ForeignKey("folio.id"), nullable=True)
    #main_folio = db.relationship("Folio")

=======
    members = db.relationship("User", secondary=team_members, backref="teams")
>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
    administrators = db.relationship("User", secondary=team_administrators)
    private = db.Column(db.Boolean(), default=False, nullable=False)

    # Company
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company")


class Folio(SlugMixin, db.Model):
    """
    A folio contains the actual documentation within a team. A folio can have projects or
    pages tied to it, all within the nolij service. 
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
<<<<<<< HEAD
    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"))
    executive = db.Column(db.Boolean(),db.ForeignKey("executive_board"))
    team = db.relationship("Team")
=======
>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
    slug = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    administrators = db.relationship("User", secondary=folio_administrators)

<<<<<<< HEAD
=======
    # Set up team relationship
    team_id = db.Column(db.Integer(), db.ForeignKey("team.id"))
    team = db.relationship("Team")


class PageQuery(BaseQuery, SearchQueryMixin):
    pass


>>>>>>> 691fcdc85a3369e8d1b10f797164e17002503566
class Page(SlugMixin, db.Model):
    """
    A Page is the model that contains the actual content. The text field
    is the field that contains the markdown text. It belongs to a folio.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)  # Title
    text = db.Column(db.UnicodeText(), nullable=True)  # Markdown Text
    date_created = db.Column(db.DateTime(), default=func.now(), nullable=False)
    date_modified = db.Column(db.DateTime(), onupdate=func.now(), nullable=False, default=func.now())
    main_page = db.Column(db.Boolean(), default=False, nullable=False)
    contributors = db.relationship("User", secondary=page_contribs)

    # Set up folio relationship
    folio_id = db.Column(db.Integer(), db.ForeignKey("folio.id"), nullable=False)
    folio = db.relationship("Folio", backref=db.backref("pages"))

    # Set up Search
    query_class = PageQuery
    search_vector = db.Column(TSVectorType('name', 'text'))

    def users_with_access(self):
        return [member.id for member in self.folio.team.members]


# ****************************** Event Listeners for Slugs ******************************

@listens_for(Folio, 'before_insert')
def folio_slug(mapper, connect, target):
<<<<<<< HEAD
    target.generate_slug()
=======
    target.generate_slug(target.name)


>>>>>>> bc6f77ce17aabf4b5b42e166187a51b07f3e032e
@listens_for(Page, 'before_insert')
def page_slug(mapper, connect, target):
    target.generate_slug(target.name)


@listens_for(Team, 'before_insert')
def page_slug(mapper, connect, target):
    target.generate_slug(target.name)
