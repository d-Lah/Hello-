import jwt
import os
import datetime
import json
from sqlalchemy import insert
from functools import wraps
from flask import Flask, request, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from . import create_app
from .db import get_db, db_session
from first_app.models import User, Post
app = create_app()
def login_required(f):
    @wraps(f)
    def _wrapper(*args,**kwargs):
        
        user_id = int(kwargs.get("user_id"))
        access_token = request.headers.get("Authorization")
        payload = jwt.decode(access_token, app.config['SECRET_KEY'], algorithms='HS256')
        token_user_id = payload["user_id"]
        
        if not token_user_id or user_id != token_user_id:
            return {"error":"Користувач не авторизований"}, 403
        
        user = User.query.filter(User.id==token_user_id).one()
        #db = get_db()
        #user = db.execute(
        #    "SELECT * FROM user WHERE id = ?",
        #    (token_user_id,),
        #).fetchone()

        if not user:
            return {"error": f"Користувач не існує {user_id}"}, 404
        if int(token_user_id) != user.id:
            return{"error": "Користувач створює не свій пост"}, 403
        
        return f(*args, **kwargs)
    return _wrapper
    
@app.route("/api/v1/register-user", methods=['GET','POST'])
def registrate_user_api():
    data = request.json
    phone_number = data["phone_number"]
    first_name = data["first_name"]
    second_name = data["second_name"]
    password = data["password"]
    new_user = User(phone_number,
                    first_name,
                    second_name,
                    generate_password_hash(password))
    db_session.add(new_user)
    db_session.commit()
    #db = get_db()
    #db.execute(
    #    "INSERT INTO user (phone_number, first_name, second_name, password) VALUES (?, ?, ?, ?)",
    #    (phone_number, first_name, second_name, generate_password_hash(password)),
    #)
    #db.commit()
    return {}, 200


@app.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json # Analog

    income_phone_number = data.get("phone_number") # Данні з запиту
    income_password = data.get("password") # Данні з запиту

    if not income_phone_number or not income_password:
        return "", 401

    #db = get_db()
    #user = db.execute(
    #    "SELECT * FROM user WHERE phone_number = ?",
    #    (income_phone_number,),
    #).fetchone()
    if income_phone_number != User.phone_number:
        return{"error":"!"} 
    user = User.query.filter(User.phone_number==income_phone_number).one()
    # Перевірка, чи користувач існує
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user.password,income_password):
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 404
    token_data = {"user_id": user.id}
    access_token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return {"access_token": access_token}, 200

@app.route("/api/v1/user-info/<user_id>", methods=['GET','POST'])
@login_required
def user_info_api(user_id):
    #db = get_db()
    #user = db.execute(
    #"SELECT * FROM user WHERE id =?",
    #(user_id,),
    #).fetchone()
    user = User.query.filter(User.id==user_id).one()
    return {"info": user.user_info()},200

@app.route("/api/v1/create-post/<user_id>", methods=["POST"])
@login_required
def create_post_api(user_id):
    db = get_db()
    data = request.json
    author_id = user_id
    title = data['title']
    body = data['body']
    current_datetime = datetime.datetime.today() 
    error = None

    if not title:
        error = 'Title is required.'
    if error is not None:
        flash(error)
    else:
        new_post = Post(author_id,current_datetime,title,body)
        db_session.add(new_post)
        db_session.commit()
        #db.execute(
        #    'INSERT INTO post (title, body, author_id)'
        #    ' VALUES (?, ?, ?)',
        #    (title, body, author_id)
        #)
        #db.commit()

    return "Опубліковано", 200
@app.route("/api/v1/user-posts/<user_id>", methods=["GET", "POST"])
@login_required
def user_post_api(user_id):
    db = get_db()
    income_author_id = user_id
    posts_db = Post.query.filter(Post.author_id==income_author_id).all()
    #post_db = db.execute(
    #    "SELECT * FROM post WHERE author_id=?",
    #    (author_id,),
    #).fetchall()
    posts = []
    for post in posts_db:
        posts.append({
            "author id": post.author_id,
            "title": post.title,
            "body": post.body,
            "created": post.created
        })
    return posts, 200
@app.route("/api/v1/delet-post/<user_id>", methods=["GET","POST"])
@login_required
def delet_post_api(user_id):
    data = request.json
    income_title = data["title"]
    post = Post.query.filter(Post.author_id==user_id).all()
    for post_title in post:
        if income_title == post_title.title:    
            Post.query.filter(Post.title == income_title).delete()
            db_session.commit()
            return {}, 200
        else:
            return {"error":"error"}
@app.route("/api/v1/update-post/<user_id>", methods=["GET","POST"])
@login_required
def update_post_api(user_id):
    data = request.json
    income_title = data["title"]
    update_title = data["update_title"]
    update_body = data["update_body"]
    update_datatime = datetime.datetime.now()
    post = Post.query.filter(Post.author_id==user_id).all()
    for post_title in post:
        if income_title == post_title.title:
            Post.query.filter(Post.title == income_title).update({"title": update_title, "body": update_body, "created": update_datatime},synchronize_session=False)
            db_session.commit()
            return {"return":"onovleno"},200
        else:
            return {"error":"error"}