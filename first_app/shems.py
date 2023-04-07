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
            raise ValidationError({"error": "Wrong post id"})
        
    @validates("text")
    def validate_text(self, text):
        if not text:
            raise ValidationError({"error": "Not text"})
        
    @validates("id")
    def validate_id(self, id):
        comment = Comment.query.filter(Comment.id==id).first()
        if not comment:
            raise ValidationError({"error":"Wrong comment id"})

class FileUploadSchema(ma.Schema):
    class Meta:
        model = FileUpload
        load_instance = True

    id = fields.Int()
    url = fields.Str()
    post_id = fields.Int()
    deleted = fields.Bool()

    @validates("id")
    def validate_id(self, id):
        exists = db.session.query(FileUpload.query.filter(FileUpload.id==id).exists()).scalar()
        if not exists:
            raise ValidationError({"error": "Wrong image id"})

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
    file = fields.Nested(FileUploadSchema)
    comments = fields.Nested(CommentSchema, many=True)

    @validates("id")
    def validate_id(self, id):
        post = Post.query.filter(Post.id==id).first()
        if not post:
            raise ValidationError({"error": "Wrong post id"})

    @validates("title")
    def validate_title(self, data, **kwargs):
        if not data["title"]:
            raise ValidationError({"error":"not title"})
    
    @validates("body")
    def validate_body(self, data, **kwargs):
        if not data["body"]:
            raise ValidationError({"error":"not body"})