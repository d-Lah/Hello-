import os
from werkzeug.utils import secure_filename
from first_app.models import FileUpload
from .login_required import login_required
from flask import Flask, g, request, render_template, flash, Blueprint
from ..db import db
from ..config import UPLOAD_FOLDER
file_upload = Blueprint("file_upload",__name__)
@file_upload.route("/api/v1/upload-file",
                   methods=["POST"])
def files_upload():
    if request.method == "POST":
        uploaded_files = request.files['file']
        if uploaded_files == '':
            return{"error":"error"}
        path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_files.filename)))
        file = FileUpload(url = uploaded_files.filename)
        db.session.add(file)
        db.session.commit()
        return{"status":"Uploaded"}
    