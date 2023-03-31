import os
from first_app.db import db
from first_app.config import UPLOAD_FOLDER
from first_app.models import FileUpload
from werkzeug.utils import secure_filename
from flask import Flask, g, request, Blueprint
file_upload = Blueprint("file_upload",__name__)
@file_upload.route("/api/v1/upload-file",
                   methods=["POST"])
def files_upload():
        
        
        uploaded_files = request.files.get('file')
        if not uploaded_files:
            return{"error":uploaded_files}, 400
        post_id = request.form.get("post_id")
        if not post_id:
            return{"error": "error"},400
        path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_files.filename)))
        file = FileUpload(url = uploaded_files.filename, post_id = post_id)
        db.session.add(file)
        db.session.commit()
        
        return {"status":"Uploaded",
               "id": file.id}
    