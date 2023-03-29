import datetime
from first_app.db import db
from first_app.config import SECRET_KEY
from .login_required import login_required
from first_app.shems import PostSchema, CommentSchema
from first_app.models import Post, FileUpload, Comment, User
from flask import Flask, g, request, render_template, flash, Blueprint
post_urls = Blueprint("psot",__name__)
schema = PostSchema(many=True)
schema_comment = CommentSchema(many=True)
@post_urls.route("/api/v1/create-post/",
                 methods=["POST"])
@login_required
def create_post_api():

    user = User.query.filter(User.id==g.user_id).one()
    
    author_id = g.user_id
    author_name = user.first_name
    data = request.json
    title = data.get('title')
    body = data.get('body')
    current_datetime = datetime.datetime.today() 
    file_id = data.get('file_id')
    
    if not title:    
        return {"error": "немає title"},400
    if not body: 
        return {"error": "немає  body"},400
    
    if file_id is None:
        new_post = Post(author_id,
                    current_datetime,
                    title,
                    body,
                    file_id=file_id,
                    user_name=author_name)
        db.session.add(new_post)
        db.session.commit()    
        return {"status":"Published"}, 200
    file = FileUpload.query.filter(FileUpload.id == file_id).first()

    if not file:
        return{"error":"error"}
    new_post = Post(author_id,
                    current_datetime,
                    title,
                    body,
                    file_id=file.id)
    db.session.add(new_post)
    db.session.commit()    
    
    return {"status":"Published"}, 200

@post_urls.route("/api/v1/user-posts",
                 methods=["GET"])
@login_required
def user_post_api():
    
    income_author_id = g.user_id
    
    posts = Post.query.filter(Post.deleted==False, Post.author_id==income_author_id).all()
    user_posts = schema.dump(posts)
    
    return {"posts":user_posts}, 200

@post_urls.route("/api/v1/delete-post/delete/<int:post_id>",
                 methods=["DELETE"])
@login_required
def delete_post_api(post_id):
    data = request.json

    author_id = g.user_id
    post = Post.query.filter(Post.id==post_id, Post.author_id==author_id).first()
    if not post:
        return{"error":"Wrong post_id or author_id"},400
    
    post.deleted = 1
    db.session.add(post)
    db.session.commit()
    
    return {"status":"Deleted"}, 200

@post_urls.route("/api/v1/update-post/update/<int:post_id>",
                 methods=["PUT"])
@login_required
def update_post_api(post_id):
    data = request.json
    update_title = data.get("update_title")
    update_body = data.get("update_body")
    update_datatime = datetime.datetime.now()
    author_id = g.user_id

    post = Post.query.filter(Post.id==post_id, Post.author_id==author_id).first()
    if not post:
        return{"error":"Wrong post_id"},400
    
    post.title = update_title
    post.body = update_body
    post.datatime = update_datatime
    db.session.add(post)
    db.session.commit()
    
    return{"status": "Update"},200

@post_urls.route("/api/v1/post-comments/post/<int:post_id>",
                    methods=["GET"])
@login_required
def post_comments_api(post_id):
    
    post = Post.query.filter(Post.deleted== False,
                             Post.id == post_id).first()
    if not post:
        return{"error":"Wrong post_id"},400
    
    post_comments = Comment.query.filter(Comment.post_id == post_id,
                                       Comment.deleted == False).all()
    comments = schema_comment.dump(post_comments)

    return {"post":{
            "author_id": post.author_id,
            "user_name": post.user_name,
            "title": post.title,
            "body": post.body,
            "created": post.created
            },
            "comments": comments}, 200
