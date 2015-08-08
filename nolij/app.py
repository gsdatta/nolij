from flask import Flask, g, request
from flask_security import Security
from nolij.database import db

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

    app = Flask(name)
    app.config.from_object(env_configs[env])

    import logging.config
    if app.config.get('LOGGING'):
        logging.config.dictConfig(app.config['LOGGING'])

    # Initialize tables and database session
    db.init_app(app)
    with app.app_context():
        db.create_all()

    security = Security(app, user_datastore)

    # Register Blueprints
    from api.auth.controllers import AUTH
    from api.studygroup.controllers import STUDY_GROUP
    # app.register_blueprint(AUTH, url_prefix='/api/auth')
    # app.register_blueprint(STUDY_GROUP, url_prefix='/api/studygroup')
    return app
