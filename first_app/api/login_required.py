import os
import jwt
import json
from first_app.db import db
from functools import wraps
from first_app.models import User
from first_app.config import SECRET_KEY
from flask import Flask, g, request, Blueprint

def login_required(f):
    @wraps(f)
    def _wrapper(*args,**kwargs):
        
        access_token = request.headers.get("Authorization")
        
        if not access_token:
            return{"error_access_token":"error"}
        splited_token = access_token.split(" ")
        
        if not splited_token[1]:
           return{"error_not_splited_token":"Not bearer"}
        
        payload = jwt.decode(splited_token[1], SECRET_KEY, algorithms='HS256')
        token_user_id = payload["user_id"]
       
        if not token_user_id:
            return {"error_user_token":"User doesn't login"}, 400
        
        user = User.query.filter(User.id==token_user_id).first()
        
        if not user:
            return {"error": "Not user"}, 400
        g.user_id = token_user_id
        
        return f(*args, **kwargs)
    return _wrapper