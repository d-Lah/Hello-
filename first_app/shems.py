from flask_marshmallow import Marshmallow
from .models import User, Post, Comment, FileUpload

ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        model = User
        load_instance = True
        fields = ("phone_number","first_name","second_name")

class PostSchema(ma.Schema):
    class Meta:
        model = Post
        load_instance = True
        fields = ("author_id","created","body","title","deleted","file_id")
        
class CommentSchema(ma.Schema):
    class Meta:
        model = Comment
        load_instance = True
        fields = ("author_id","post_id","created","text","deleted")
        
class FileUploadSchema(ma.Schema):
    class Meta:
        model = FileUpload
        load_instance = True
        fields = ("url",),