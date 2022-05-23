from flask import render_template
from bson.objectid import ObjectId
from cocktails import app, db
from cocktails.models import Category, Users


@app.route("/")
def home():
    return render_template("base.html")
