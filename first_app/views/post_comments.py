from flask import Flask, g, request, render_template, flash, Blueprint

post_comments = Blueprint("post_comments",__name__)
@post_comments.route("/post-comments/post/<int:post_id>", methods=["GET"])
def post_comments_view(post_id):
    return render_template('post_comments.html')