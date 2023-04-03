import os

from flask import Flask
from first_app.db import db
from flask_migrate import Migrate
from first_app.views.index import index
from first_app.views.login import login
from first_app.api.user import user_urls
from first_app.api.post import post_urls
from first_app.api.comment import comment_urls
from first_app.api.file_upload import file_upload
from first_app.views.registrate import registrate
from first_app.views.user_posts import user_posts
from first_app.views.create_post import create_post
from first_app.views.create_comment import create_comment
from first_app.views.post_comments import post_comments
from first_app.views.user_info_edit import user_info_edit

basedir = os.path.abspath(os.path.dirname(__file__))

# /home/im/Hello-/first_app/ -> Dynamic os.path.join(basedir,'data.sqlite')
UPLOAD_FOLDER = os.path.join(basedir, "uploads")

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
    app.register_blueprint(index)
    app.register_blueprint(registrate)
    app.register_blueprint(login)
    app.register_blueprint(create_post)
    app.register_blueprint(user_posts)
    app.register_blueprint(create_comment)
    app.register_blueprint(post_comments)
    app.register_blueprint(user_info_edit)
    return app

if __name__=='__main__':
    create_app().run(debug=True)