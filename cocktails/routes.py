from flask import (
    flash, render_template,
    request, redirect, session, url_for)
from bson.objectid import ObjectId
from cocktails import app, db, mongo
from cocktails.models import Category, Users


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)
