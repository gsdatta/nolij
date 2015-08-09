from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.auth.forms import ExtendedRegisterForm
from nolij.auth.models import user_datastore, User
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
    if request.method == 'GET':
        return render_template("root/signup.html")

    if request.method == 'POST':
        comp = Company.query.filter_by(domain=request.form['company_domain']).first()
        if comp is None:
            comp = Company(name=request.form['company_name'], domain=request.form['company_domain'])
            db.session.add(comp)
            db.session.commit()

        return redirect(url_for('root.user_signup'))


@ROOT.route('user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template('root/user_signup.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['user_name']
        domain = email.split('@')[1]

        comp = Company.query.filter_by(domain=domain).first()
        if comp is None:
            flash("Company doesn't exist, please create one first")
            return redirect(url_for('root.company_signup'))

        user = user_datastore.create_user(email=email, password=password, name=name, company_id=comp.id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('root.login'))


@ROOT.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
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

    return render_template("security/login.html", form=form)


@ROOT.route('logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('root.index'))

