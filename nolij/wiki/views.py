from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.database import db
from nolij.auth.models import user_datastore, User
from nolij.company.models import Company
from nolij.wiki.models import Team, Wiki, Page, slugify
from flask_login import current_user, login_required


WIKI = Blueprint('wiki', __name__)

@WIKI.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    teams = Team.query.filter_by(company_id=current_user.company_id).all()
    return render_template("wiki/dashboard.html", teams=teams)

@WIKI.route('/add_team', methods=['GET', 'POST'])
@login_required
def add_team():
    if request.method == 'POST':
        name = request.form['name']

        new_team = Team(name=name, company_id=current_user.company_id, slug=slugify(name))

        new_team.members.append(current_user)
        new_team.administrators.append(current_user)

        db.session.add(new_team)
        db.session.commit()

        if 'wikis' in request.form and request.form['wikis']:
            wikis = request.form['wikis'].split(',')
            current_app.logger.info(wikis)
            for wiki in wikis:
                new_wiki = Wiki(name=wiki, description='', team_id=new_team.id, slug=slugify(wiki))
                new_wiki.administrators.append(current_user)

                db.session.add(new_wiki)
            db.session.commit()

        return redirect(url_for('wiki.dashboard'))

@WIKI.route('/<team_slug>', methods=['GET', 'POST'])
@login_required
def team_details(team_slug):
    if request.method == 'GET':
        team = Team.query.filter_by(slug=team_slug).first()
        wikis = Wiki.query.filter_by(team_id=team.id).all()

        return render_template("wiki/team_details.html", wikis=wikis, team_slug=team.slug)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        team = Team.query.filter_by(slug=team_slug).first()

        new_wiki = Wiki(name=name, description=description, team_id=team.id, slug=slugify(name))
        new_wiki.administrators.append(current_user)

        db.session.add(new_wiki)
        db.session.commit()
        return redirect(url_for('wiki.team_details', team_slug=team.slug))

@WIKI.route('/<team_slug>/<wiki_slug>', methods=['GET', 'POST'])
@login_required
def wiki_details(team_slug, wiki_slug):
    if request.method == 'GET':
        team = Team.query.filter_by(slug=team_slug).first()
        wiki = Wiki.query.filter_by(slug=wiki_slug).first()

        if team is None or wiki is None:
            flash('That team or wiki does not exist. Please create it')
            return redirect(url_for('wiki.dashboard'))

        return render_template("wiki/wiki_details.html", wiki=wiki, team=team)

