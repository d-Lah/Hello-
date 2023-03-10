import os
from flask import Flask
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='templates', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import db
    db.init_app(app)
    migrate = Migrate(app, db)
    return app
if __name__=='__main__':
    create_app().run(debug=True)
