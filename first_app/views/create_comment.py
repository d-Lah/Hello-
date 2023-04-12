from flask import Flask, g, request, render_template, flash, Blueprint

create_comment = Blueprint("create_comment",__name__)
@create_comment.route("/create-comment/post/<int:post_id>", methods=["GET"])
def create_comment_view(post_id):
    return render_template('create_comment.html')