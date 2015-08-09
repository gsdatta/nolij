from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.company.forms import CompanyForm
from nolij.auth.models import user_datastore, User
from nolij.auth.forms import UserRegistrationForm
from nolij.company.models import Company
from nolij.database import db
from flask_security.forms import LoginForm
from flask_security.views import login_user
from flask_security.utils import verify_password
from flask_login import current_user

import bcrypt

ROOT = Blueprint('root', __name__)


@ROOT.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for("folio.dashboard"))
    else:
        return render_template("root/index.html")


@ROOT.route('company_signup', methods=['GET', 'POST'])
def company_signup():
    form = CompanyForm()
    if form.validate_on_submit():
        comp = Company(name=form.name.data, domain=form.domain.data)
        db.session.add(comp)
        db.session.commit()
        flash('Awesome, you have a company created!')
        return redirect(url_for('root.user_signup'))

    return render_template("root/signup.html", company_form=form)


@ROOT.route('user_signup', methods=['GET', 'POST'])
def user_signup():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        domain = email.split('@')[1]

        # Get the company corresponding to this domain.
        comp = Company.query.filter_by(domain=domain).first()

        # If the company doesn't exist, send them to company signup
        if comp is None:
            flash("Company doesn't exist, please create one first")
            return redirect(url_for('root.company_signup'))

        # Otherwise, try to create the user
        user = user_datastore.create_user(email=email, password=password, name=name, company_id=comp.id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('root.login'))

    return render_template('root/user_signup.html', signup_form=form)


@ROOT.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Try to get a user to get with email being signed in with
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # If the user exists, check their password and authenticate them
            if verify_password(form.password.data.encode('utf-8'), user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember.data)
                return redirect(url_for("folio.dashboard"))
            else:
                flash('Incorrect username or password')
                return render_template("security/login.html", form=form)
        else:
            flash('Incorrect username or password')
            return render_template("security/login.html", form=form)

    return render_template("security/login.html", login_form=form)


@ROOT.route('logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('root.index'))

