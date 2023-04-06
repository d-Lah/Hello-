import datetime
from first_app.db import db
from marshmallow import ValidationError
from first_app.config import SECRET_KEY
from .login_required import login_required
from first_app.models import Post, Comment, User
from first_app.shems import PostSchema, CommentSchema
from flask import Flask, g, request, render_template, flash, Blueprint

comment_urls = Blueprint("comment",__name__)

@comment_urls.route("/api/v1/create-comment/post/<int:post_id>",
                    methods=["POST"])
@login_required
def create_comment_api(post_id):
  
    user = User.query.filter(User.id==g.user_id).one()

    data = request.json
    author_id = g.user_id
    author_name = user.first_name
    comments_post_id = post_id
    text = data.get("text")
    created = datetime.datetime.now()
    
    error = CommentSchema().validate({"text": text, "post_id": comments_post_id})
    
    error_post_id = error.get("post_id")
    error_text = error.get("text")
    
    if error_post_id:
        return error_post_id, 404
    
    if error_text: 
        return error_text, 400
    
    new_comment = Comment(author_id,
                    comments_post_id,
                    created,
                    text,
                    user_name=author_name)
    db.session.add(new_comment)
    db.session.commit()    
    
    return {"status":"Published"}, 200

@comment_urls.route("/api/v1/delete-comment/delete/<int:comment_id>",
                    methods=["DELETE"])
@login_required
def delete_comment_post_api(comment_id):
    data = request.json  
    author_id = g.user_id
    comment = Comment.query.filter(Comment.id==comment_id,
                                   Comment.author_id==author_id).first()
    if not comment:
        return{"error":"Wrong comment_id or author_id"},400
    
    comment.deleted = 1
    db.session.add(comment)
    db.session.commit()
    
    return {"status":"Deleted"}, 200

@comment_urls.route("/api/v1/update-comment/update/<int:comment_id>",
                    methods=["PUT"])
@login_required
def update_comment_post_api(comment_id):
    data = request.json
    update_text = data.get("text")
    update_datatime = datetime.datetime.now()
    author_id = g.user_id
    
    error = CommentSchema().validate({"id": comment_id})
    if error:
        return{"error":"Wrong comment or author_id"},404
    
    comment = Comment.query.filter(Comment.id == comment_id,
                                   Comment.author_id == author_id).first()
    
    comment.text = update_text
    comment.datatime = update_datatime
    db.session.add(comment)
    db.session.commit()
    
    return{"status": "Update"},200