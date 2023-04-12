from flask import Flask, g, request, render_template, flash, Blueprint

create_post = Blueprint("create_post",__name__)
@create_post.route("/create-post", methods=["GET"])
def create_post_view():
    return render_template('create_post.html')