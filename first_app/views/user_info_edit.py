from flask import Flask, g, request, render_template, flash, Blueprint

user_info_edit = Blueprint("user_info_edit",__name__)
@user_info_edit.route("/user-info/edit", methods=["GET"])
def user_info_edit_view():
    return render_template('user_info_edit.html')