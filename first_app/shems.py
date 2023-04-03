from .db import db
from flask_marshmallow import Marshmallow
from .models import User, Post, Comment, FileUpload
from marshmallow import fields, validates, validates_schema, ValidationError
ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        model = User
        load_instance = True

    id = fields.Int()
    phone_number = fields.Int()
    first_name = fields.Str()
    second_name = fields.Str()

class CommentSchema(ma.Schema):
    class Meta:
        model = Comment
        load_instance = True

    id = fields.Int()
    author_id = fields.Int()
    post_id = fields.Int()
    user_name = fields.Str()
    created = fields.DateTime()
    text = fields.Str()
    deleted = fields.Bool()

    @validates("post_id")
    def validate_post_id(self, post_id):
        exists = db.session.query(Post.query.filter(Post.id==post_id).exists()).scalar()
        if not exists:
            raise ValidationError({"error": "Wrong post id"}, status_code=404)
        
    @validates("text")
    def validate_text(self, text):
        if not text:
            raise ValidationError({"error": "Not text"}, status_code=400)

class FileUploadSchema(ma.Schema):
    class Meta:
        model = FileUpload
        load_instance = True

    id = fields.Int()
    url = fields.Str()
    post_id = fields.Int()

class PostSchema(ma.Schema):
    class Meta:
        model = Post
        load_instance = True

    id = fields.Int()
    author_id = fields.Int()
    user_name = fields.Str()
    created = fields.DateTime()
    body = fields.Str()
    title = fields.Str()
    deleted = fields.Bool()
    file = fields.Nested(FileUploadSchema(only=("id","url")), many=True)
    comments = fields.Nested(CommentSchema, many=True)

    @validates_schema
    def validate_title_or_body(self, title, body):
        if not title or not body:
            raise ValidationError("not title or body")