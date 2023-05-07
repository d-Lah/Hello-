from flask import Flask, g, request, render_template, flash, Blueprint

post_with_comments = Blueprint("post_with_comments",__name__)
@post_with_comments.route("/post/<int:post_id>", methods=["GET"])
def post_with_comments_view(post_id):
    return render_template('post_with_comments.html')