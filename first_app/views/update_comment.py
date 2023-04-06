from flask import Flask, g, request, render_template, flash, Blueprint

update_comment = Blueprint("update_comment",__name__)
@update_comment.route("/update-comment/update/<int:comment_id>", methods=["GET"])
def update_post_view(comment_id):
    return render_template('update_comment.html')