from flask import Flask, g, request
from flask_security import Security
from nolij.database import db
from flask.ext.markdown import Markdown

def create_app(name, env):
    """
    This creates an app according to the factory pattern outlined in:
    http://flask.pocoo.org/docs/0.10/patterns/appfactories/

    This will help for development/production configs as well as Gunicorn
    deployment.
    """

    env_configs = {
        'dev': 'nolij.config.DevelopmentConfig',
        }

    app = Flask(name, static_folder='views/static', template_folder='views/templates')
    app.config.from_object(env_configs[env])


    import logging.config
    if app.config.get('LOGGING'):
        logging.config.dictConfig(app.config['LOGGING'])

    from nolij.root.views import ROOT
    from nolij.folio.views import FOLIO

    app.register_blueprint(ROOT, url_prefix='/')
    app.register_blueprint(FOLIO, url_prefix='/folio')

    from nolij.auth.models import User, user_datastore
    from nolij.company.models import Company
    from nolij.folio.models import Team, Folio, Page

    # Initialize tables and database session
    db.init_app(app)
    with app.app_context():
        db.create_all()

    security = Security(app, user_datastore)

    Markdown(app)

    # Register Blueprints
    return app
