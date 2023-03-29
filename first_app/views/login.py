from flask import Flask, g, request, render_template, flash, Blueprint

login = Blueprint("login",__name__)

@login.route("/login", methods=["GET"])
def login_view():
    return render_template('login.html')