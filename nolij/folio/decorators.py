from flask import request, flash, url_for, current_app, redirect
from flask_login import current_user
from nolij.folio.models import Team, Folio, Page
from functools import wraps

def team_access(f):
    @wraps(f)
    def decorated_function(team_slug, *args, **kwargs):
        team = Team.query.filter_by(slug=team_slug).first()
        if team is None:
            flash('Team does not exist')
            return redirect(url_for('folio.dashboard'))
        if current_user not in team.members:
            flash('You do not have permission to view this team')
            return redirect(url_for('folio.dashboard'))
        else:
            request.team = team

        return f(team_slug, *args, **kwargs)
    return decorated_function

def folio_access(f):
    @wraps(f)
    def decorated_function(team_slug, folio_slug, *args, **kwargs):
        folio = Folio.query.filter_by(slug=folio_slug).first()
        if folio is None:
            flash('Folio does not exist')
            return redirect(url_for('folio.dashboard'))
        else:
            request.folio = folio

        return f(team_slug, folio_slug, *args, **kwargs)
    return decorated_function

def page_access(f):
    @wraps(f)
    def decorated_function(team_slug, folio_slug, page_slug, *args, **kwargs):
        page = Page.query.filter_by(slug=page_slug).first()
        if page is None:
            flash('Page does not exist')
            return redirect(url_for('folio.dashboard'))
        else:
            request.page = page

        return f(team_slug, folio_slug, page_slug, *args, **kwargs)
    return decorated_function
