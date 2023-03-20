import datetime
from first_app.db import db
from first_app.config import SECRET_KEY
from .login_required import login_required
from first_app.models import Post, FileUpload
from flask import Flask, g, request, render_template, flash, Blueprint

post_urls = Blueprint("psot",__name__)

@post_urls.route("/api/v1/create-post/<int:user_id>",
                 methods=["POST"])
@login_required
def create_post_api(user_id):
    data = request.json
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    
    author_id = g.user_id
    title = data['title']
    body = data['body']
    current_datetime = datetime.datetime.today() 
    file_id = data['file_id']
    
    if not title:    
        return {"error": "немає title"},400
    if not body: 
        return {"error": "немає  body"},400
    
    if file_id == None:
        new_post = Post(author_id,
                    current_datetime,
                    title,
                    body,
                    file_id=file_id)
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

@post_urls.route("/api/v1/user-posts/<int:user_id>",
                 methods=["GET"])
@login_required
def user_post_api(user_id):
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    
    income_author_id = g.user_id
    posts_db = Post.query.filter(Post.deleted==False and Post.author_id==income_author_id).all()
    posts = []
    for post in posts_db:
        posts.append({
            "author id": post.author_id,
            "title": post.title,
            "body": post.body,
            "file_id": post.file_id,
            "created": post.created
        })
    
    return {"posts":posts}, 200

@post_urls.route("/api/v1/delete-post/<int:user_id>/delete/<int:post_id>",
                 methods=["DELETE"])
@login_required
def delete_post_api(user_id, post_id):
    data = request.json  
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    
    author_id = g.user_id
    post = Post.query.filter(Post.id==post_id and Post.author_id==author_id).first()
    if not post:
        return{"error":"Wrong post_id or author_id"},400
    
    post.deleted = 1
    db.session.add(post)
    db.session.commit()
    
    return {"status":"Deleted"}, 200

@post_urls.route("/api/v1/update-post/<int:user_id>/update/<int:post_id>",
                 methods=["PUT"])
@login_required
def update_post_api(user_id, post_id):
    data = request.json
    update_title = data["update_title"]
    update_body = data["update_body"]
    update_datatime = datetime.datetime.now()
    author_id = g.user_id
    
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    post = Post.query.filter(Post.id==post_id and Post.author_id==author_id).first()
    if not post:
        return{"error":"Wrong post_id or author_id"},400
    
    post.title = update_title
    post.body = update_body
    post.datatime = update_datatime
    db.session.add(post)
    db.session.commit()
    
    return{"status": "Update"},200
