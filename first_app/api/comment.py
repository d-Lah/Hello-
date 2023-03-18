import datetime
from first_app.db import db
from first_app.config import SECRET_KEY
from .login_required import login_required
from first_app.models import Post, Comment
from flask import Flask, g, request, render_template, flash, Blueprint

comment_urls = Blueprint("comment",__name__)

@comment_urls.route("/api/v1/create-comment/<int:user_id>/post/<int:post_id>",
                    methods=["POST"])
@login_required
def create_comment_api(user_id, post_id):
    data = request.json
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    author_id = g.user_id
    comments_post_id = post_id
    text = data["text"]
    created = datetime.datetime.now()
    if not text:    
        return {"error": "немає text"},400
    comment = Comment(author_id,
                    comments_post_id,
                    created,
                    text)
    db.session.add(comment)
    db.session.commit()    
    return {"status":"Published"}, 200

@comment_urls.route("/api/v1/post-comments/post/<int:post_id>",
                    methods=["GET"])
@login_required
def post_comments_api(post_id):
    income_author_id = g.user_id
    post = Post.query.filter(Post.deleted== False,
                             Post.id == post_id).first()
    if not post:
        return{"error":"Wrong post_id"},400
    comments_db = Comment.query.filter(Comment.post_id == post_id,
                                       Comment.deleted == False).all()
    comments = []
    
    for comment in comments_db:
        comments.append({
            "author id": comment.author_id,
            "text": comment.text,
            "created": comment.created
        })
    
    return {"post":{
            "author id": post.author_id,
            "title": post.title,
            "body": post.body,
            "created": post.created
            },
            "comments": comments}, 200

@comment_urls.route("/api/v1/delete-comment/<int:user_id>/delete/<int:comment_id>",
                    methods=["DELETE"])
@login_required
def delete_comment_post_api(user_id, comment_id):
    data = request.json  
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    author_id = g.user_id
    comment = Comment.query.filter(Comment.id==comment_id,
                                   Comment.author_id==author_id).first()
    if not comment:
        return{"error":"Wrong comment_id or author_id"},400
    
    comment.deleted = 1
    db.session.add(comment)
    db.session.commit()
    
    return {"status":"Deleted"}, 200

@comment_urls.route("/api/v1/update-comment/<int:user_id>/update/<int:comment_id>",
                    methods=["PUT"])
@login_required
def update_comment_post_api(user_id, comment_id):
    data = request.json
    update_text = data["text"]
    update_datatime = datetime.datetime.now()
    author_id = g.user_id
    
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    comment = Comment.query.filter(Comment.id == comment_id,
                                   Comment.author_id == author_id).first()
    if not comment:
        return{"error":"Wrong comment or author_id"},400
    
    comment.text = update_text
    comment.datatime = update_datatime
    db.session.add(comment)
    db.session.commit()
    
    return{"status": "Update"},200