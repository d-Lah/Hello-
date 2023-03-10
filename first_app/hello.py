import jwt
import os
import datetime
import json
from sqlalchemy import insert
from functools import wraps
from flask import Flask, g, request, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from . import create_app
from .db import get_db, db_session
from first_app.models import User, Post
app = create_app()
def login_required(f):
    @wraps(f)
    def _wrapper(*args,**kwargs):
        
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms='HS256')
        token_user_id = payload["user_id"]
        
        if not token_user_id:
            return {"error":"Користувач не авторизований"}, 400
        user = User.query.filter(User.id==token_user_id).first()
        if not user:
            return {"error": f"Користувач не існує"}, 400
        g.user_id = token_user_id
        
        return f(*args, **kwargs)
    return _wrapper
    
@app.route("/api/v1/register-user", methods=['POST'])
def registrate_user_api():
    data = request.json
    phone_number = data["phone_number"]
    first_name = data["first_name"]
    second_name = data["second_name"]
    password = data["password"]
    exists = db_session.query(User.query.filter(User.phone_number==phone_number).exists()).scalar()
    if exists:
        return{"error:":"Phone number already exists"}, 400
    if not phone_number or first_name:
        return{"error":"Немає номеру телефона, або ім'я "}, 400
    new_user = User(phone_number,
                    first_name,
                    second_name,
                    generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()
    return {}, 200

@app.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json
    income_phone_number = data.get("phone_number")
    income_password = data.get("password")

    if not income_phone_number or not income_password:
        return {"error":"Not phone number or password"}, 400    
    user = User.query.filter(User.phone_number==income_phone_number).first()
    if not user:
        return {"error":"Невірний номер телефону, або пароль"},400
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user.password,income_password):
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 400
    token_data = {"user_id": user.id}
    access_token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return {"access_token": access_token}, 200

@app.route("/api/v1/user-info/<int:user_id>", methods=['GET'])
@login_required
def user_info_api(user_id):
    if user_id != g.user_id:
        return{"error": "Request data isn't yours"},400
    user = User.query.filter(User.id==g.user_id).first()
    if not user:
        return{"error": "Request data isn't yours"},400
    return {"info": user.user_info()},200

@app.route("/api/v1/user-info/edit/<int:user_id>", methods=['PUT'])
@login_required
def user_profile_edit(user_id):
    if user_id != g.user_id:
        return{"error": "Request data isn't yours"}
    data = request.json
    new_phone_number = data["phone_number"]
    new_first_name = data["first_name"]
    new_second_name = data["second_name"]
    exists = db_session.query(User.query.filter(User.phone_number==new_phone_number).exists()).scalar()
    if exists:
        return{"error:":"Phone number already exists"}, 400
    user = User.query.filter(User.id==user_id).first()
    if not user:
        return{"error": "Request data isn't yours"},400
    user.phone_number = new_phone_number
    user.first_name = new_first_name
    user.second_name = new_second_name
    db_session.commit()
    return{"status":"Update"},400

@app.route("/api/v1/user-info/change-password/<int:user_id>", methods=['PUT'])
@login_required
def change_password(user_id):
    if user_id != g.user_id:
        return{"error": "Request data isn't yours"},400
    data = request.json
    old_password = data["old_password"]
    new_password = data["new_password"]
    user = User.query.filter(User.id==g.user_id).first()
    if not user: 
        return{"error":"Request data isn't yours"},400
    if not check_password_hash(user.password,old_password):
        return{"error":"Wrong old password"},400
    if not new_password:
        return{"error":"Немає нового паролю"},400
    
    user.password = generate_password_hash(new_password) 
    db_session.commit()
    return{"status":"Update"},200

@app.route("/api/v1/create-post/<int:user_id>", methods=["POST"])
@login_required
def create_post_api(user_id):
    data = request.json
    if user_id != g.user_id:
        return{"error":"Request data isn't yours"},400
    author_id = g.user_id
    title = data['title']
    body = data['body']
    current_datetime = datetime.datetime.today() 
    if not title:    
        return {"error": "немає title"},400
    if not body:
        return {"error": "немає  body"},400
    new_post = Post(author_id,
                    current_datetime,
                    title,
                    body)
    db_session.add(new_post)
    db_session.commit()    
    return {"status":"Published"}, 200

@app.route("/api/v1/user-posts/<int:user_id>", methods=["GET"])
@login_required
def user_post_api(user_id):
    db = get_db()
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
            "created": post.created
        })
    return {"posts":posts}, 200

@app.route("/api/v1/delete-post/<int:user_id>/delete/<int:post_id>", methods=["DELETE"])
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
    db_session.add(post)
    db_session.commit()
    return {"status":"Deleted"}, 200
@app.route("/api/v1/update-post/<int:user_id>/update/<int:post_id>", methods=["PUT"])
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
    db_session.add(post)
    db_session.commit()
    return{"status": "Update"},200