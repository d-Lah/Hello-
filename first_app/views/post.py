from flask import Flask, g, request, render_template, flash, Blueprint

post = Blueprint("post",__name__)
@post.route("/post/<int:post_id>", methods=["GET"])
def post_comments_view(post_id):
    return render_template('post.html')