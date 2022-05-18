![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome rhysmoggs,

This is the Code Institute student template for Gitpod. We have preinstalled all of the tools you need to get started. It's perfectly ok to use this template as the basis for your project submissions.

You can safely delete this README.md file, or change it for your own project. Please do read it at least once, though! It contains some important information about Gitpod and the extensions we use. Some of this information has been updated since the video content was created. The last update to this file was: **September 1, 2021**

## Gitpod Reminders

To run a frontend (HTML, CSS, Javascript only) application in Gitpod, in the terminal, type:

`python3 -m http.server`

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

To run a backend Python file, type `python3 app.py`, if your Python file is named `app.py` of course.

A blue button should appear to click: _Make Public_,

Another blue button should appear to click: _Open Browser_.

In Gitpod you have superuser security privileges by default. Therefore you do not need to use the `sudo` (superuser do) command in the bash terminal in any of the lessons.

To log into the Heroku toolbelt CLI:

1. Log in to your Heroku account and go to *Account Settings* in the menu under your avatar.
2. Scroll down to the *API Key* and click *Reveal*
3. Copy the key
4. In Gitpod, from the terminal, run `heroku_config`
5. Paste in your API key when asked

You can now use the `heroku` CLI program - try running `heroku apps` to confirm it works. This API key is unique and private to you so do not share it. If you accidentally make it public then you can create a new one with _Regenerate API Key_.

------



deployment

1. use template from CI
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
6. create a folder with the same name as your database (in this case, folder is named "cocktails") in the root of your project.
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
14. create a new file "base.html" within the "templates" folder
15. within the "base.html" file, write whatever you wish to be presented on your website.
16. in the terminal, write `python3 run.py` to launch the project 