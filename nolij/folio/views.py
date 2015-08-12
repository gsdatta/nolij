from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.database import db
from nolij.auth.models import user_datastore, User
from nolij.company.models import Company
from nolij.folio.models import Team, Folio, Page, slugify
from nolij.folio.decorators import folio_access_control
from nolij.folio.forms import TeamForm
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
    form = TeamForm(private=True)
    form.private.data = form.private.data or False
    if form.validate_on_submit():
        new_team = Team(name=form.name.data, company_id=current_user.company_id, private=form.private.data)

        # Update members and admins
        new_team.members.append(current_user)
        new_team.administrators.append(current_user)

        # Save the new team
        db.session.add(new_team)
        db.session.commit()

        return redirect(url_for('folio.dashboard'))
    else:
        current_app.logger.info([field.errors for field in form])
    return render_template('team/new_team.html', new_team_form=form)


@FOLIO.route('/<team_slug>', methods=['GET', 'POST', 'PUT'])
@login_required
@folio_access_control(layers=['team'])
def team_details(team_slug):
    if request.method == 'GET':
        folios = Folio.query.filter_by(team_id=request.team.id).all()

        return render_template("team/team_details.html", folios=folios, team=request.team)

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
@folio_access_control(layers=['team', 'folio'])
def folio_details(team_slug, folio_slug):
    if request.method == 'GET':
        team = request.team
        folio = request.folio

        if team is None or folio is None:
            flash('That team or folio does not exist. Please create it')
            return redirect(url_for('folio.dashboard'))

        page = Page.query.filter_by(folio_id=folio.id, main_page=True).first()
        return render_template("page/page_details.html", folio=folio, team=team, page=page)


@FOLIO.route('/<team_slug>/<folio_slug>/new', methods=['GET', 'POST'])
@login_required
@folio_access_control(layers=['team', 'folio'])
def new_page(team_slug, folio_slug):
    if request.method == 'GET':
        return render_template('page/new_page.html', folio=request.folio, team=request.team)

    if request.method == 'POST':
        if 'title' not in request.form or 'content' not in request.form or request.form['title'] == '':
            # TODO: Send text back if only the title is fucked up so they don't lose their work
            flash('Missing a title or content')
            return render_template('page/new_page.html', folio=request.folio, team=request.team)

        title = request.form['title']
        main_page = (title == 'Overview')
        new_page = Page(folio_id=request.folio.id, name=title, text=request.form['content'], main_page=main_page)

        new_page.contributors.append(current_user)

        db.session.add(new_page)
        db.session.commit()

        return redirect(url_for('folio.folio_details', team_slug=request.team.slug, folio_slug=request.folio.slug))


@FOLIO.route('/<team_slug>/<folio_slug>/<page_slug>', methods=['GET', 'POST'])
@login_required
@folio_access_control(layers=['team', 'folio', 'page'])
def page_details(team_slug, folio_slug, page_slug):
    if request.method == 'GET':
        return render_template("page/page_details.html", folio=request.folio, team=request.team, page=request.page)


@FOLIO.route('/<team_slug>/settings', methods=['GET'])
@login_required
@folio_access_control(layers=['team'])
def team_settings(team_slug):
    form = TeamForm()
    form.name.data = request.team.name
    form.private.data = request.team.private
    return render_template('team/settings.html', team=request.team, new_team_form=form)


@FOLIO.route('/search', methods=['POST'])
@login_required
def search():
    if request.search_form.validate_on_submit():
        return redirect(url_for('folio.search_results', query=request.search_form.query.data))


@FOLIO.route('/search/<query>', methods=['GET'])
def search_results(query):
    results = Page.query.search(query).all()
    # results = (db.session.query(Page, Folio, Team)
    #     .join(Team)
    #     .join(Folio)
    #     .filter()
    #            )
    # results = Page.query.filter(Page.folio.team.has(current_user in Team.members)).search(query).all()
    current_app.logger.info(results)
    return render_template('search/results.html', results=results)
