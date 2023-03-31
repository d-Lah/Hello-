from marshmallow import fields
from flask_marshmallow import Marshmallow
from .models import User, Post, Comment, FileUpload

ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        model = User
        load_instance = True
    
    phone_number = fields.Int()
    first_name = fields.Str()
    second_name = fields.Str()

class CommentSchema(ma.Schema):
    class Meta:
        model = Comment
        load_instance = True
    
    author_id = fields.Int()
    post_id = fields.Int()
    user_name = fields.Str()
    created = fields.DateTime()
    text = fields.Str()
    deleted = fields.Bool()
        
class FileUploadSchema(ma.Schema):
    class Meta:
        model = FileUpload
        load_instance = True

    url = fields.Str()
    post_id = fields.Int()

class PostSchema(ma.Schema):
    class Meta:
        model = Post
        load_instance = True

    author_id = fields.Int()
    user_name = fields.Str()
    created = fields.DateTime()
    body = fields.Str()
    title = fields.Str()
    deleted = fields.Bool()
    file = fields.Nested(FileUploadSchema, many=True)