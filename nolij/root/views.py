from flask import Blueprint, render_template, request, current_app, jsonify, flash
from nolij.auth.forms import ExtendedRegisterForm
from nolij.auth.models import user_datastore
from nolij.company.models import Company
from nolij.database import db

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
