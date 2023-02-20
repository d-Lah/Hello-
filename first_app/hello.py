import jwt
import time
import os
import json
from functools import wraps
from flask import Flask, request, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from . import create_app
from .db import get_db
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
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?",
            (token_user_id,),
        ).fetchone()

        if not user:
            return {"error": f"Користувач не існує {user_id}"}, 404
        if int(token_user_id) != user["id"]:
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

    db = get_db()
    db.execute(
        "INSERT INTO user (phone_number, first_name, second_name, password) VALUES (?, ?, ?, ?)",
        (phone_number, first_name, second_name, generate_password_hash(password)),
    )
    db.commit()
    return {}, 200


@app.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json # Analog

    income_phone_number = data.get("phone_number") # Данні з запиту
    income_password = data.get("password") # Данні з запиту

    if not income_phone_number or not income_password:
        return "", 401

    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE phone_number = ?",
        (income_phone_number,),
    ).fetchone()
    # Перевірка, чи користувач існує
    if not user:
        return {"error": f"Користувач не існує з телефоном {income_phone_number}"}, 404

    if not check_password_hash(user["password"],income_password):
        return {"error": f"Паролі не співпадають {income_phone_number}"}, 404
    token_data = {"user_id": user["id"]}
    access_token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return {"access_token": access_token}, 200
@app.route("/api/v1/user-info/<user_id>", methods=['GET','POST'])
@login_required
def user_info_api(user_id):
    db = get_db()
    user = db.execute(
    "SELECT * FROM user WHERE id =?",
    (user_id,),
    ).fetchone()
    return{
        "id": user["id"],
        "phone_number": user["phone_number"],
        "first_name": user["first_name"],
        "second_name": user["second_name"]
    },200

@app.route("/api/v1/create-post/<user_id>", methods=["POST"])
@login_required
def create_api(user_id):
    db = get_db()
    data = request.json
    author_id = user_id
    title = data['title']
    body = data['body']
    error = None

    if not title:
        error = 'Title is required.'
    if error is not None:
        flash(error)
    else:
        db.execute(
            'INSERT INTO post (title, body, author_id)'
            ' VALUES (?, ?, ?)',
            (title, body, author_id)
        )
        db.commit()

    return "Опубліковано", 200
@app.route("/api/v1/user-posts/<user_id>", methods=["GET", "POST"])
@login_required
def user_post_api(user_id):
    db = get_db()
    author_id = user_id
    post_db = db.execute(
        "SELECT * FROM post WHERE author_id=?",
        (author_id,),
    ).fetchall()
    posts = []
    for post in post_db:
        posts.append({
            "id": post["id"],
            "title": post["title"],
            "body": post["body"],
            "created": post["created"],
        })
    return posts, 200
@app.route("/", methods=["GET", "POST"])
def biba():
    return "lalala", 200
#    title = data['title']
#    body = data['body']
#    error = None
#
#    if not title:
#        error = 'Title is required.'
#    if error is not None:
#        flash(error)
#    else:
#        db = get_db()
#        db.execute(
#            'INSERT INTO post (title, body, author_id)'
#            ' VALUES (?, ?, ?)',
#            (title, body, author_id)
#        )
#        db.commit()


#    title = data["title"]
#    body = data["body"]
#    db.execute(
#        'INSERT INTO post (title, body, author_id)'
#        'VALUES (?, ?, ?)',
#    (title, body, author_id)
#    )
#    db.commit