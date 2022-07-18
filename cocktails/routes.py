from flask import flash, render_template, request, redirect, session, url_for
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from cocktails import app, db, mongo
from cocktails.models import Category, Users


# @app.route("/")
# @app.route("/home")
# def home():
#     cocktails = list(mongo.db.cocktails.find())
#     return render_template("home.html", cocktails=cocktails)


@app.route("/")
@app.route("/home")
def home():
    categories = list(Category.query.order_by(Category.category_name).all())
    cocktails = list(mongo.db.cocktails.find())
    return render_template("home.html", cocktails=cocktails, categories=categories)


# @app.route('/')
# def index():
#     page, per_page, offset = get_page_args(page_parameter='page',
#                                            per_page_parameter='per_page')
#     total = len(users)
    # pagination_users = get_users(offset=offset, per_page=per_page)
    # pagination = Pagination(page=page, per_page=per_page, total=total,
    #                         css_framework='materializecss')
    # return render_template('index.html',
    #                        users=pagination_users,
    #                        page=page,
    #                        per_page=per_page,
    #                        pagination=pagination,
    #                        )


# users = list(range(100))



# def get_users(offset=0, per_page=10):
#     return users[offset: offset + per_page]


@app.route("/all_cocktails")
def all_cocktails():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 9
    offset = (page - 1) * per_page
    cocktails = list(mongo.db.cocktails.find())
    total = len(cocktails)
    cocktails_paginated = cocktails[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materializecss')
    return render_template("all_cocktails.html",
                           cocktails=cocktails_paginated,
                        #    users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


# @app.route("/filter_category/<int:category_id>")
# def filter_category(category_id):
#     cocktails = list(mongo.db.cocktails.find({"category_id": str(category_id)}))
#     return render_template("filter_category.html",  cocktails=cocktails)


@app.route("/filter_category/<int:category_id>")
def filter_category(category_id):
    category = Category.query.get_or_404(category_id)
    # this below works, but pulls all categories for filter_category.html
    # categories = list(Category.query.order_by(Category.category_name).all())
    cocktails = list(mongo.db.cocktails.find({"category_id": str(category_id)}))
    # return render_template("filter_category.html",  cocktails=cocktails)
    return render_template("filter_category.html",  category=category, cocktails=cocktails)


@app.route("/search")
def search():
    query = request.args.get("query")
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 9
    offset = (page - 1) * per_page
    cocktails = list(mongo.db.cocktails.find({"$text": {"$search": query}}))
    total = len(cocktails)
    cocktails_paginated = cocktails[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='materializecss')
    return render_template("all_cocktails.html",
                           cocktails=cocktails_paginated,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


# @app.route("/search", methods=["GET", "POST"])
# def search():
#     query = request.form.get("query")
#     cocktails = list(mongo.db.cocktails.find({"$text": {"$search": query}}))
#     return render_template("all_cocktails.html", cocktails=cocktails)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        #check to see if passwords match or not:
        if request.form.get("password") != request.form.get("confirm-password"):
            flash("Passwords do not match. Please tyry again.")
            return redirect(url_for("register"))

        # create a dictionary
        user = Users(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
        )

        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        # flash("Registration Successful!")
        flash("Registration Successful! Welcome, {}".format(
                            request.form.get("username")))
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = Users.query.filter(Users.user_name == \
                                           request.form.get("username").lower()).all()

        if existing_user:
            print(request.form.get("username"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                # better for brute forcing by not hinting which is incorrect.
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    if "user" in session:
        cocktails = list(mongo.db.cocktails.find())
        return render_template("profile.html", username=session["user"], cocktails=cocktails)

    # if session["user"] == "admin":
    #     cocktails = list(mongo.db.cocktails.find())
    #     return render_template("profile.html", username=session["user"], cocktails=cocktails)
    

    # if session["user"] == "admin" or "user" in session:
    #     cocktails = list(mongo.db.cocktails.find())
    #     return render_template("profile.html", username=session["user"], cocktails=cocktails)

    return redirect(url_for("login"))


###########################################################################################################
## test begins here for deleting user
###########################################################################################################


# use post method? if POST:
# @app.route("/delete_user/<username>") use post and get
# def delete_user(username):
#     if "user" not in session:
#         flash("You must be logged in to use this function.")
#         return redirect(url_for("all_cocktails"))

#     user = Users.query.get_or_404(username)
#     print(user)
#     db.session.delete(user)
#     db.session.commit()
#     mongo.db.cocktails.delete_many({"created_by": str(username)})
#     flash("User Deleted")
#     return redirect(url_for("login.html"))


###########################################################################################################
## test ends here for deleting user
###########################################################################################################


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_cocktail", methods=["GET", "POST"])
def add_cocktail():
    if "user" not in session:
        flash("You need to be logged in to add a cocktail")
        return redirect(url_for("all_cocktails"))

    if request.method == "POST":
        cocktail = {
            "category_id": request.form.get("category_id"),
            "cocktail_name": request.form.get("cocktail_name"),
            "cocktail_img": request.form.get("cocktail_img"),
            "cocktail_description": request.form.get("cocktail_description"),
            "main_ingredient": request.form.get("main_ingredient"),
            "created_by": session["user"],
            "method": request.form.getlist("method"),
            "other_ingredient": request.form.getlist("other_ingredient"),
            "prep_time": request.form.get("prep_time"),
            "servings": request.form.get("servings")
        }
        mongo.db.cocktails.insert_one(cocktail)
        flash("Cocktail Successfully Added")
        return redirect(url_for("all_cocktails"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("add_cocktail.html", categories=categories)


@app.route("/edit_cocktail/<cocktail_id>", methods=["GET", "POST"])
def edit_cocktail(cocktail_id):

    cocktail = mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)})

    if "user" not in session or session["user"] != cocktail["created_by"]:
        flash("You can only edit your own cocktails!")
        return redirect(url_for("all_cocktails"))

    if request.method == "POST":
        submit = {
            "category_id": request.form.get("category_id"),
            "cocktail_name": request.form.get("cocktail_name"),
            "cocktail_img": request.form.get("cocktail_img"),
            "cocktail_description": request.form.get("cocktail_description"),
            "main_ingredient": request.form.get("main_ingredient"),
            "created_by": session["user"],
            "method": request.form.getlist("method"),
            "other_ingredient": request.form.getlist("other_ingredient"),
            "prep_time": request.form.get("prep_time"),
            "servings": request.form.get("servings")
        }
        mongo.db.cocktails.update_one({"_id": ObjectId(cocktail_id)}, {"$set": submit})
        flash("Cocktail Successfully Updated")
        return redirect(url_for("all_cocktails"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("edit_cocktail.html", cocktail=cocktail, categories=categories)


@app.route("/delete_cocktail/<cocktail_id>")
def delete_cocktail(cocktail_id):

    cocktail = mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)})

    if "user" not in session or session["user"] != cocktail["created_by"]:
        flash("You can only delete your own cocktails!")
        return redirect(url_for("all_cocktails"))

    mongo.db.cocktails.delete_one({"_id": ObjectId(cocktail_id)})
    flash("Cocktail Successfully Deleted")
    return redirect(url_for("all_cocktails"))


# @app.route("/view_cocktail/<cocktail_id>")
# def view_cocktail(cocktail_id):

#     cocktail = mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)})
#     return render_template("view_cocktail.html", cocktail=cocktail)


@app.route("/view_cocktail/<cocktail_id>")
def view_cocktail(cocktail_id):

    cocktail = mongo.db.cocktails.find_one({"_id": ObjectId(cocktail_id)})
    # others = mongo.db.cocktails.find_one("other_ingredient")
    # print(others)
    return render_template("view_cocktail.html", cocktail=cocktail)


@app.route("/get_categories")
def get_categories():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("all_cocktails"))

    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():

    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("all_cocktails"))

    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        flash("New Category Added")
        return redirect(url_for("get_categories"))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("all_cocktails"))

    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        flash("Category Updated")
        return redirect(url_for("get_categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    if session["user"] != "admin":
        flash("You must be admin to manage categories!")
        return redirect(url_for("all_cocktails"))

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    mongo.db.cocktails.delete_many({"category_id": str(category_id)})
    flash("Category Deleted")
    return redirect(url_for("get_categories"))


# Error handling
# 400 error page is displayed
@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400


# 401 error page is displayed
@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401


# 404 error page is displayed
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# 405 error page is displayed
@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


# 500 error page is displayed
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
