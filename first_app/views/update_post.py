from flask import Flask, g, request, render_template, flash, Blueprint

update_post = Blueprint("update_post",__name__)
@update_post.route("/user-posts/update/<int:post_id>", methods=["GET"])
def update_post_view(post_id):
    return render_template('update_post.html')