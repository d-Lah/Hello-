from flask import Flask, g, request, render_template, flash, Blueprint

change_password = Blueprint("change_password",__name__)
@change_password.route("/user-info/change-password", methods=["GET"])
def change_password_view():
    return render_template('change_password.html')