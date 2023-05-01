import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY='dev'
MEDIA_FOLDER = "media"
BLOG_IMAGE_FOLODER = "media/blog_images"
UPLOAD_FOLDER = os.path.join(basedir, BLOG_IMAGE_FOLODER)
ALLOWED_EXTENSIONS = ["png","jpg","jpeg","gif"]