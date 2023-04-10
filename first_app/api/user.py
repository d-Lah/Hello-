import os
import jwt
import json
from first_app.db import db
from first_app.models import User
from first_app.shems import UserSchema
from first_app.config import SECRET_KEY
from flask import g, request, Blueprint
from .login_required import login_required
from werkzeug.security import check_password_hash, generate_password_hash
user_urls = Blueprint("sync",__name__)

@user_urls.route("/api/v1/register-user", methods=['POST'])
def registrate_user_api():
    data = request.json
    phone_number = data.get("phone_number")
    first_name = data.get("first_name")
    second_name = data.get("second_name")
    password = data.get("password")
    
    error = UserSchema().validate({
        "phone_number" : phone_number,
        "first_name" : first_name,
        "second_name" : second_name,
        "password" : password
    })
    if error:
        return{"error": error},

    exists = db.session.query(User.query.filter(User.phone_number==phone_number).exists()).scalar()
    if exists:
        return{"error:":"Phone number already exists"}, 400
    
    new_user = User(phone_number,
                    first_name,
                    second_name,
                    generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    
    return {}, 200

def login_user(user):
    token_data = {"user_id": user.id}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm='HS256')
    return access_token

@user_urls.route("/api/v1/login", methods=['POST'])
def login_api():
    data = request.json
    income_phone_number = data.get("phone_number")
    income_password = data.get("password")
    
    if not income_phone_number or not income_password:
        return {"error":"Not phone number or password"}, 400
 
    user = User.query.filter(User.phone_number==income_phone_number).first()
    
    if not user:
        return {"error":"Wrong phone number or password"},400
    
    if not check_password_hash(user.password,income_password):
        return {"error": f"Wrong phone number or password"}, 400

    access_token = login_user(user)

    return {"access_token": access_token}, 200

@user_urls.route("/api/v1/user-info",
                  methods=['GET'])
@login_required
def user_info_api():

    user = User.query.filter(User.id==g.user_id).first()
    if not user:
        return{"error": "Request data isn't yours"},400
    
    return {"info": user.full_name()},200

@user_urls.route("/api/v1/user-info/edit",
                  methods=['PUT'])
@login_required
def user_profile_edit():

    data = request.json
    new_phone_number = data.get("phone_number")
    new_first_name = data.get("first_name")
    new_second_name = data.get("second_name")
    
    exists = db.session.query(User.query.filter(User.phone_number==new_phone_number).exists()).scalar()
    if exists:
        return{"error:":"Phone number already exists"}, 400
    
    user = User.query.filter(User.id==g.user_id).first()
    if not user:
        return{"error": "Request data isn't yours"},400
    
    if new_phone_number:
        user.phone_number = new_phone_number
    
    if new_first_name:
        user.first_name = new_first_name
    
    if new_second_name:
        user.second_name = new_second_name
    
    db.session.commit()
    
    return{"status":"Update"},200

@user_urls.route("/api/v1/user-info/change-password",
                  methods=['PUT'])
@login_required
def change_password():
    
    data = request.json
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    user = User.query.filter(User.id==g.user_id).first()
    
    if not user: 
        return{"error":"Request data isn't yours"},400
    
    if not check_password_hash(user.password,old_password):
        return{"error_old_password":"Wrong old password"},400
    
    if not new_password:
        return{"error":"Not new password"},400
    
    user.password = generate_password_hash(new_password) 
    db.session.commit()
    
    return{"status":"Changed"},200