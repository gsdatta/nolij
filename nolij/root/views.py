from flask import Blueprint, render_template, request, current_app, jsonify, flash, redirect, url_for
from nolij.auth.forms import ExtendedRegisterForm
from nolij.auth.models import user_datastore, User
from nolij.company.models import Company
from nolij.database import db
from flask_security.forms import LoginForm
from flask_security.views import login_user

import bcrypt

ROOT = Blueprint('root', __name__)


@ROOT.route('/')
def index():
    return render_template("root/index.html")


@ROOT.route('signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        current_app.logger.info('Entering signup')
        return render_template("root/signup.html", form=ExtendedRegisterForm())

    if request.method == 'POST':
        comp = Company.query.filter_by(domain=request.form['company_domain']).first()
        if comp is None:
            comp = Company(name=request.form['company_name'], domain=request.form['company_domain'])
            db.session.add(comp)
            db.session.commit()

            user = user_datastore.create_user(email=request.form['email'], password=request.form['password'], name=request.form['user_name'], company_id=comp.id)

            return jsonify(user.as_dict())
        else:
            flash('Company already exists with that domain')
            return render_template("root/signup.html")


@ROOT.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    current_app.logger.info(form.data)
    if form.validate_on_submit():
        current_app.logger.info('VALIDATING')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("root.index"))
            else:
                flash('Incorrect username or password')
                return render_template("security/login.html", form=form)
        else:
            flash('Incorrect username or password')
            return render_template("security/login.html", form=form)

    return render_template("security/login.html", form=form)
