

technologies used:

- PsycoPG2 - database adapter. library for connecting Python to PostgreSQL.
- SQLAlchemy - ORM lirbary


data schema:

link both together through...


    relational database:


    PostgreSQL - open-source, Object-Relational Databse Management System (ORDBMS). fre use, licencing? good for future projects or launching this one if needs be.

    primary key - A unique ID that identifies individual records regardless of any changes that occur



    non-relational:
    mongoDB - 


------



deployment of website:

1. use template from CI / copy this projects link/url?
2. install two python packages. Flask and SQLAlchemy to work with Postgres databases. psycopg2 is necessary to work with Postgres database. In command line type: `pip3 install Flask-SQLAlchemy psycopg2`
3. create "env.py" file
4. make sure to have a .gitignore file and add env.py to that if not using CI's original template. All hidden and sensitive files/folders to be added here.
5. in "env.py", type following:
    ```
    import os

    os.environ.setdefault("IP", "0.0.0.0")
    os.environ.setdefault("PORT", "5000")
    os.environ.setdefault("SECRET_KEY", "any_secret_key")
    os.environ.setdefault("DEBUG", "True")
    os.environ.setdefault("DEVELOPMENT", "True")
    os.environ.setdefault("DB_URL", "postgresql:///cocktails")
    ```

    The `any_secret_key` can be called whatever you wish: `os.environ.setdefault("SECRET_KEY", "any_secret_key")`

    make sure to change `os.environ.setdefault("DEBUG", "True")` to "False" before deploying/launching project.

    os.environ.setdefault("DB_URL", "postgresql:///cocktails") points to the databse to be created, in this case "cocktails".
6. create a folder (in this case, folder is named "cocktails") in the root of your project.
7. within that newly created folder, create a file called "__init__.py"
8. write the following in the new file:
    ```
    import os
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    if os.path.exists("env.py"):
        import env  # noqa


    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

    db = SQLAlchemy(app)

    from cocktails import routes  # noqa
    ```
9. create a "routes.py" file within the "cocktails" folder
10. within that "routes.py" file, write the following:
    ```
    from flask import render_template
    from cocktails import app, db


    @app.route("/")
    def home():
        return render_template("base.html")
    ```
11. in root of project, create "run.py" file
12. within "run.py", write the following:
    ```
    import os
    from cocktails import app


    if __name__ == "__main__":
        app.run(
            host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG")
        )
    ```
13. within "cocktails" folder, create a new "templates" folder. This is where Flask will search for any html templates to be rendered.
14. create a new file "base.html" within the "templates" folder.
15. within the "base.html" file, write whatever you wish to be presented on your website.
16. in the terminal, write `python3 run.py` to launch the project.
17. commit and push


Setting up Databse:

make sure you have postgreSQL installed locally if you are not using CI's template?
set up the databse schema as follows:
1. define our models by creating a "models.py" file within the "cocktails" folders
2. write the following in the "models.py" file and create the tables:
    ```
    from cocktails import db


    class Category(db.Model):
        # schema for the Category model
        id = db.Column(db.Integer, primary_key=True)
        category_name = db.Column(db.String(25), unique=True, nullable=False)

        def __repr__(self):
            # __repr__ to represent itself in the form of a string
            return self.category_name


    class Users(db.Model):
        # schema for the Task model
        id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(20), unique=True, nullable=False)
        password = db.Column(db.String(260), nullable=False)

        def __repr__(self):
            # __repr__ to represent itself in the form of a string
            return self.user_name
    ```
3. in "routes.py", import these newly created models:
    ```
    from cocktails.models import Category, Users
    ```
4.  log in to postgreSQL terminal
5. CREATE DATABASE cocktails