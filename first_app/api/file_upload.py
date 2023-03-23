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
        
        uploaded_files = request.files['file']
        if uploaded_files == '':
            return{"error":"error"}
        
        path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_files.filename)))
        file = FileUpload(url = uploaded_files.filename)
        db.session.add(file)
        db.session.commit()
        
        return{"status":"Uploaded"}
    