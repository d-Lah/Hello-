

from flask import Flask, g, request, render_template, flash, Blueprint

index = Blueprint("index",__name__)

@index.route("/", methods=["GET"])
def index_view():
    return render_template('index.html')

@index.route("/login", methods=["GET"])
def login_view():
    return render_template('login.html')