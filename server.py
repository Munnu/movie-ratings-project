"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

# @app.route("/login-page", methods=["GET", "POST"])
# def login_page():
#     email = request.form.get("email")
#     password = request.form.get("password")
#     return render_template("sign_up.html",
#                             email=email,
#                             password=password)

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """Sign up"""

    email = request.form.get("email")
    password = request.form.get("password")
    print "This is request email and password", email, password

    email_login_query = User.query.filter_by(email=email).first()
    # check to see if email_login_query is empty
    if not email_login_query:
        # okay then, we go create a new user by populating the database
        new_user = User()
        # set the User instance's email and password (we call it new_user)
        new_user.email = email
        new_user.password = password

        # add new user to the session, database insertion
        db.session.add(new_user)
        db.session.commit()
    else:
        # exist, we should sign them in at some point
        print "You're already a user, silly!"

    return render_template("sign_up.html",
                            email=email,
                            password=password)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
