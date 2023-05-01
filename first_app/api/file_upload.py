import os
from uuid import uuid4
from first_app.db import db
from first_app.models import FileUpload
from werkzeug.utils import secure_filename
from first_app.shems import FileUploadSchema
from first_app.constans import FileStatuses, FileTypes
from first_app.api.login_required import login_required
from flask import request, Blueprint, g, send_from_directory
from first_app.config import (
    UPLOAD_FOLDER, 
    MEDIA_FOLDER,
    BLOG_IMAGE_FOLODER,
    ALLOWED_EXTENSIONS) 

def validate_file(func):
    def _wrapper(*args, **kwargs):
        uploaded_file = request.files.get('file')
        
        if not uploaded_file:
            return{"error_file_upload":"Not file"}, 400

        file_name, file_ext = uploaded_file.filename.split(".")

        if file_ext not in ALLOWED_EXTENSIONS:
            return{"error_file_ext":"Wrong file extension"}, 400
        
        g.file_name = file_name
        g.file_ext = file_ext

        return func(*args, **kwargs)
    return _wrapper

def _handel_file_upload(
        user_id,file_name,
        file_ext,
        file_type,
        saving_file):
    
    filename = f"{file_name}-{uuid4()}.{file_ext}"
    saving_file.save(os.path.join(
        f"{UPLOAD_FOLDER}/{user_id}",
        secure_filename(filename)))
    
    url = f"{BLOG_IMAGE_FOLODER}/{user_id}/{filename}"
    file = FileUpload(
        url = url,
        author_id = user_id,
        file_type = file_type)
    
    db.session.add(file)
    db.session.commit()
    return file

file_upload = Blueprint("file_upload",__name__)

@file_upload.route("/api/v1/upload-file",
                   methods=["POST"])
@login_required
@validate_file
def files_upload():

    user_id = g.user_id
    uploaded_files = request.files.get('file')

    file_name = g.file_name
    file_ext = g.file_ext

    file = _handel_file_upload(
        user_id,
        file_name,
        file_ext,
        FileTypes.BLOG_MAIN_PICTURE,
        uploaded_files)

    return {"status":FileStatuses.UPLOADED,
           "id": file.id}

@file_upload.route("/api/v1/delete-file",
                   methods=["DELETE"])
def file_delete():
    image_id = request.form.get("image_id")
    error = FileUploadSchema().validate({"id": image_id})
    if error:
        return {"error": "Wrong post id"}, 404
    
    file = FileUpload.query.filter(FileUpload.id==image_id).one()
    file.deleted = 1
    db.session.add(file)
    db.session.commit()
    
    return {"status":FileStatuses.DELETED}, 200

@file_upload.route("/media/<path:path>")
def download_image(path):
    return send_from_directory(MEDIA_FOLDER, path), 200

@file_upload.route("/post/media/<path:path>")
def download_post_image(path):
    return send_from_directory(MEDIA_FOLDER, path), 200