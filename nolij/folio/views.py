from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.database import db
from nolij.auth.models import user_datastore, User
from nolij.company.models import Company
from nolij.folio.models import Team, Folio, Page, slugify
from nolij.folio.decorators import team_access
from flask_login import current_user, login_required


FOLIO = Blueprint('folio', __name__)

@FOLIO.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    teams = Team.query.filter_by(company_id=current_user.company_id).all()
    return render_template("folio/dashboard.html", teams=teams)

@FOLIO.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == 'POST':
        name = request.form['name']

        new_team = Team(name=name, company_id=current_user.company_id, slug=slugify(name))

        new_team.members.append(current_user)
        new_team.administrators.append(current_user)

        db.session.add(new_team)
        db.session.commit()

        if 'folios' in request.form and request.form['folios']:
            folios = request.form['folios'].split(',')
            current_app.logger.info(folios)
            for folio in folios:
                new_folio = Folio(name=folio, description='', team_id=new_team.id, slug=slugify(folio))
                new_folio.administrators.append(current_user)

                db.session.add(new_folio)
            db.session.commit()

        return redirect(url_for('folio.dashboard'))

@FOLIO.route('/<team_slug>', methods=['GET', 'POST', 'PUT'])
@login_required
@team_access
def team_details(team_slug):
    if request.method == 'GET':
        folios = Folio.query.filter_by(team_id=request.team.id).all()
        current_app.logger.info(request.team)

        return render_template("folio/team_details.html", folios=folios, team=request.team)

    if request.method == 'POST':
        if 'add_user' in request.form:
            if 'users' in request.form:
                user_emails = request.form['users'].split()
                for email in user_emails:
                    user = User.query.filter_by(email=email).first()
                    if user is None:
                        flash('User with email %s does not exist.' % email)
                        continue

                    request.team.members.append(user)
                    current_app.logger.info(request.team.members)
                    db.session.add(request.team)

                db.session.commit()
            return redirect(url_for('folio.team_details', team_slug=request.team.slug))

        name = request.form['name']
        description = request.form['description']

        new_folio = Folio(name=name, description=description, team_id=request.team.id, slug=slugify(name))
        new_folio.administrators.append(current_user)

        db.session.add(new_folio)
        db.session.commit()
        return redirect(url_for('folio.team_details', team_slug=request.team.slug))



@FOLIO.route('/<team_slug>/<folio_slug>', methods=['GET', 'POST'])
@login_required
def folio_details(team_slug, folio_slug):
    if request.method == 'GET':
        team = Team.query.filter_by(slug=team_slug).first()
        folio = Folio.query.filter_by(slug=folio_slug).first()

        if team is None or folio is None:
            flash('That team or folio does not exist. Please create it')
            return redirect(url_for('folio.dashboard'))

        return render_template("folio/folio_details.html", folio=folio, team=team)


