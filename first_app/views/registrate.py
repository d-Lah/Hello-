from flask import Flask, g, request, render_template, flash, Blueprint

registrate = Blueprint("registrate",__name__)

@registrate.route("/registrate", methods=['GET'])
def registrate_view():
    return render_template("registrate.html")