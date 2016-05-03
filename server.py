"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, \
                  redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db
from sqlalchemy.sql import and_, or_, not_


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

@app.route("/login", methods=["GET", "POST"])
def login_page():
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
        return redirect(url_for('index'))
    else:
        # information is already in the database
        # check to see if the username and password match what is in db
        username_password_check = User.query.filter(
                                                    and_(
                                                        User.email==email, 
                                                        User.password==password
                                                        )).first()
        print "\n\n\nThis is USERNAME_AND_PASSWORD_CHECK", username_password_check
        if username_password_check is None:
            print "ERROR!!!!"
        else:
            # valid login credentials redirects user to home page
            flash('You were successfully logged in')
            return redirect(url_for('index'))
            print "\n\n\n======================================"


@app.route("/sign-up")
def sign_up():
    """Sign up"""

    return render_template("sign_up.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
