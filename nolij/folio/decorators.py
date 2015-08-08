from flask import request, flash, url_for, current_app, redirect
from flask_login import current_user
from nolij.folio.models import Team
from functools import wraps

def team_access(f):
    @wraps(f)
    def decorated_function(team_slug, *args, **kwargs):
        team = Team.query.filter_by(slug=team_slug).first()
        current_app.logger.info((team.members, current_user))
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
