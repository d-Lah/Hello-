from flask_marshmallow import Marshmallow
from marshmallow import post_dump, fields
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
        fields = ("author_id","user_name","created","body","title","deleted","file")
        # author_id = fields.Int()
        # user_name = fields.String()
        # created = fields.DateTime()
        # body = fields.String()
        # title = fields.String()
        # deleted = fields.Boolean()
        # file = fields.Nested(FileUpload)
class CommentSchema(ma.Schema):
    class Meta:
        model = Comment
        load_instance = True
        fields = ("author_id","post_id","user_name","created","text","deleted")
        
class FileUploadSchema(ma.Schema):
    class Meta:
        model = FileUpload
        load_instance = True
        fields = ("url",),