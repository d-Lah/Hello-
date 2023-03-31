import os
from first_app.db import db
from flask import request, Blueprint
from first_app.models import FileUpload
from werkzeug.utils import secure_filename
from first_app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
file_upload = Blueprint("file_upload",__name__)
@file_upload.route("/api/v1/upload-file",
                   methods=["POST"])
def files_upload():
        
        
        uploaded_files = request.files.get('file')
        if not uploaded_files:
            return{"error_file_upload":"Not file"}, 400
        
        filename = uploaded_files.filename

        file_ext =  os.path.splitext(filename)[1]
        if file_ext not in ALLOWED_EXTENSIONS:
             return{"error_file_ext":"Wrong file extension"}, 400
        
        post_id = request.form.get("post_id")
        
        if not post_id:
            return{"error_post_id": "Not post"},400
        
        
        path_to_file = uploaded_files.save(os.path.join(UPLOAD_FOLDER,
                                                        secure_filename(uploaded_files.filename)))
        file = FileUpload(url = filename,
                          post_id = post_id)
        db.session.add(file)
        db.session.commit()
        
        return {"status":"Uploaded",
               "id": file.id}
    