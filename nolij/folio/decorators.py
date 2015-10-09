from flask import request, flash, url_for, current_app, redirect
from flask_login import current_user
from nolij.folio.models import Team, Folio, Page
from functools import wraps

def folio_access_control(layers=['team', 'folio', 'page']):
    """
    Decorator controls access to views based on the layers chosen.
    For each access layer, it adds the corresponding object to the request object.

    :param layers: An array of ACL's to check (team, folio, page, etc)
    :return: The decorated function
    """
    def decorated_function(f):
        @wraps(f)
        def wrapper(team_slug=None, folio_slug=None, page_slug=None, *args, **kwargs):
            slugs = {}  # Used to add the URL args to the final called function

            if 'team' in layers:
                team = Team.query.filter_by(slug=team_slug).first()
                if team is None:
                    flash('Team does not exist')
                    return redirect(url_for('folio.dashboard'))
                if current_user not in team.members and team.private == True:
                    flash('You do not have permission to view this team')
                    return redirect(url_for('folio.dashboard'))
                else:
                    request.team = team
                    slugs['team_slug'] = team_slug

            if 'folio' in layers:
                folio = Folio.query.filter_by(slug=folio_slug).first()
                if folio is None:
                    flash('Folio does not exist')
                    return redirect(url_for('folio.dashboard'))
                else:
                    request.folio = folio
                    slugs['folio_slug'] = folio_slug

            if 'page' in layers:
                page = Page.query.filter_by(slug=page_slug).first()
                if page is None:
                    flash('Page does not exist')
                    return redirect(url_for('folio.dashboard'))
                else:
                    request.page = page
                    slugs['page_slug'] = page_slug

            return f(**slugs)
        return wrapper
    return decorated_function
