from flask import Flask, g, request, render_template, flash, Blueprint

user_posts = Blueprint("user_posts",__name__)

@user_posts.route("/user-posts", methods=['GET'])
def registrate_view():
    return render_template("user_posts.html")