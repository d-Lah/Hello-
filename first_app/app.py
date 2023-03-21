import os
from .db import db
from flask import Flask
from flask_migrate import Migrate
from first_app.api.user import user_urls
from first_app.api.post import post_urls
from first_app.api.comment import comment_urls
from first_app.api.file_upload import file_upload
from flask_marshmallow import Marshmallow
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = "/home/im/Hello-/first_app/uploads"

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='templates', instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(user_urls)
    app.register_blueprint(post_urls)
    app.register_blueprint(comment_urls)
    app.register_blueprint(file_upload)
    return app

if __name__=='__main__':
    create_app().run(debug=True)