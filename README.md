

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
4. make sure to have a ".gitignore" file and add "env.py" to that if not using CI's original template. All hidden and sensitive files/folders to be added here.
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

    The `any_secret_key` can be called whatever you wish: `os.environ.setdefault("SECRET_KEY", "any_secret_key")`or generate a random and secure password here: https://randomkeygen.com/

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


Setting up Databse - postgreSQL database:

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
4.  log in to postgreSQL terminal by typing psql in terminal.
5. type `CREATE DATABASE cocktails;`
6. then `\c cocktails;` to connect to the newly created database.
7. finally `\q` to exit.
8. use python to generate and migrate the models into the database. if any changes are made to this database, you must repeat the same steps to refresh and update your database. in the terminal, type `python3`.
9. type `from cocktails import db`
10. type `db.create_all()`
11. if you wish to check that the tables exist, type `psql -d cocktails` followed by `\dt` then `\q` to quit, otherwise just exit via `exit()`.
12. commit then push


Setting up Database - MongoDB database:

Make sure to that you have a MongoDB account.

1. Create a cluster (https://www.mongodb.com/basics/clusters/mongodb-cluster-setup). This project uses a shared cluster. Choose the closest region to you which is free to use. Free cluster tier and then name your cluster ("myFirstCluster", in this project).
2. In Database Access, add a new database user (https://www.mongodb.com/docs/atlas/security-add-mongodb-users/#add-database-users).
3. In Network Access, click add IP address and choose 'Allow Access From Anywhere'. Input the IP of your hosts here to add further security.
4. In the newly created Cluster, click on Create a Database and under Database Name, enter "cocktails"
5. Under Collection, enter "recipes".
6. within the cocktails database, click on Create Collection button and enter any other collections you wish to store.
7. within each collection, click on Insert Document, and enter the key-value paris you wish to store in your document. For this project, the following key names and value data types were stored:
    ```
    cocktail_name: <string>
    category_name: <string>
    cocktail_img: <string>
    cocktail_description: <string>
    created_by: <string>
    main_ingredient: <string>
    other_ingredients: <string>
    prep_time: <string>
    servings: <Int32> with a default value of "0"
    method: <Int32> with a default value of "0"
    ```
8. In the terminal, install dnspython `pip3 install dnspython`
9. Install pymongo too `pip3 install flask-pymongo`
10. on the mongo website, in your collection, connect your cluster. Choose 'Connect your application' and choose Python and your version (3.6 or later, in this project).
11. Copy the string.
12. In the "env.py" file, add the following environment variables to the already present ones:
    ```
    os.environ.setdefault("MONGO_URI", "mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTER>-4g3i1.mongodb.net/<DATABASE>?retryWrites=true&w=majority")
    os.environ.setdefault("MONGO_DBNAME", "cocktails")
    ```
    Make sure to insert your own information for `<USERNAME>`, `<PASSWORD>`, `<CLUSTER>` and `<DATABASE>`.
13. In "__init__.py" add  `from flask_pymongo import PyMongo`.
14. Add and update:
    ```
    app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    ```
15. Add `mongo = PyMongo(app)` too.
16. In "routes.py", add and update to:
    ```
    from flask import flash, render_template, request, redirect, session, url_for
    from bson.objectid import ObjectId
    ```


Linking the databases:

1. Using category_id
2. 


Deploy the application to Heroku:

1. Create a "requirements.txt" by typing `pip3 freeze --local > requirements.txt` in the terminal. This lists what is necessary to run the project.
2. Create a Procfile by typing `echo web: python app.py > Procfile` in the terminal. In the newly created "Procfile", check to see if a blank line appears under the written code. If there is, delete and save that change. It can cause issues with Heroku.
3. Commit and push.
4. On the Heroku website. Create a new app and name it. Choose the regeion closest to you.
5. Create a new database on Heroku. Resources > Add-ons, search for heroku-postgreSQL and choose the 'Hobby Dev - Free' option, or whichever suits your needs.
6. Once confirmed, go to Settings > Config Vars > Reveal Config Vars, and input the following:
    ```
    IP = 0.0.0.0
    PORT = 5000
    SECRET_KEY = your_secret_key_here
    MONGO_URI = mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTER>-4g3i1.mongodb.net/<DATABASE>?retryWrites=true&w=majority
    MONGO_DBNAME = your_database_name_here
    ```
    You can add:
    ```
    DEBUG = True
    ```
    temporarily but make sure to change to `False` when finalizing the app. Keep to `True` for error fixing during development.
7. 