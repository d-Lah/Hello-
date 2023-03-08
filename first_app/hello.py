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
            return {"error":"Користувач не авторизований"}, 403
        try:
            user = User.query.filter(User.id==token_user_id).one()
        except: 
            return{"error": "Ви запрашуєте не свою інформацію"}
        if not user:
            return {"error": f"Користувач не існує"}, 404
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
    new_user = User(phone_number,
                    first_name,
                    second_name,
                    generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()
    return {}, 200


@app.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json # Analog

    income_phone_number = data.get("phone_number") # Данні з запиту
    income_password = data.get("password") # Данні з запиту

    if not income_phone_number or not income_password:
        return "", 401
    try:    
        user = User.query.filter(User.phone_number==income_phone_number).one()
    except:
        return {"error":"Невірний номер телефону, або пароль"}
    # Перевірка, чи користувач існує
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user.password,income_password):
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 404
    token_data = {"user_id": user.id}
    access_token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return {"access_token": access_token}, 200

@app.route("/api/v1/user-info/<int:user_id>", methods=['GET'])
@login_required
def user_info_api(user_id):
    if user_id != g.user_id:
        return{"error": "Request data isn't yours"}
    user = User.query.filter(User.id==user_id).one()
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
    User.query.filter(User.id==user_id).update({"phone_number":new_phone_number,
                                                "first_name": new_first_name,
                                                "second_name":new_second_name},
                                                synchronize_session=False)
    db_session.commit()
    return{"return":"ok"}
@app.route("/api/v1/create-post/<int:user_id>", methods=["POST"])
@login_required
def create_post_api(user_id):
    db = get_db()
    data = request.json
    if user_id == g.user_id:
        return{"error":"ви пробуєте створити не у себе пост"}
    author_id = user_id
    title = data['title']
    body = data['body']
    current_datetime = datetime.datetime.today() 
    if not title or body:    
        return {"error": "немає title або body"}
    else:
        new_post = Post(author_id,current_datetime,title,body)
        db_session.add(new_post)
        db_session.commit()
    
    return "Опубліковано", 200
@app.route("/api/v1/user-posts/<int:user_id>", methods=["GET"])
@login_required
def user_post_api(user_id):
    db = get_db()
    income_author_id = user_id
    posts_db = Post.query.filter(Post.author_id==income_author_id and Post.deleted==0).all()
    posts = []
    for post in posts_db:
        posts.append({
            "author id": post.author_id,
            "title": post.title,
            "body": post.body,
            "created": post.created
        })
    return posts, 200
@app.route("/api/v1/delete-post/<int:user_id>/delete/<int:post_id>", methods=["DELETE"])
@login_required
def delet_post_api(user_id, post_id):
    data = request.json  
    if user_id == g.user_id:
        try:
            Post.query.filter(Post.author_id == user_id and Post.id == post_id).update({"deleted":1})
            db_session.commit()
            return {}, 200
        except: 
            return{"error":"Невірний user_id або post_id"}    
    else:
        return{"error":"ви пробуєте видалити не свій пост"}
@app.route("/api/v1/update-post/<int:user_id>/update/<int:post_id>", methods=["PUT"])
@login_required
def update_post_api(user_id, post_id):
    data = request.json
    update_title = data["update_title"]
    update_body = data["update_body"]
    update_datatime = datetime.datetime.now()
    if user_id == g.user_id:
        try:
            Post.query.filter(Post.author_id==user_id and Post.id==post_id).update({"title": update_title, 
                                                                                    "body": update_body, 
                                                                                    "created": update_datatime},
                                                                                    synchronize_session=False)
            db_session.commit()
            return {"return":"onovleno"},200
        except:
            return {"error": "Невірний user_id або post_id"}
    else:
        return{"error":"ви пробуєте оновити не свій пост"}