import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY='dev'
UPLOAD_FOLDER = os.path.join(basedir, "uploads")
ALLOWED_EXTENSIONS = [".png",".jpg",".jpeg",".gif"]