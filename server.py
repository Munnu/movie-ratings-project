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

    return render_template("homepage.html",
                            user_session_info=session)


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", 
                            users=users)

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """User profile page"""

    if 'user_id' in session:
        user = User.query.filter_by(user_id=user_id).first()
        
        # Returns a list of rating objects (rating ids, user id, movie ids and scores)
        ratings_on_user_id = Rating.query.filter_by(user_id=user_id).all()

        return render_template("user-profile.html",
                                age=user.age,
                                zipcode=user.zipcode,
                                ratings_on_user_id=ratings_on_user_id
                                )


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

        if username_password_check is None:
            # want to redirect them back the the page with login form
            # flash a message
            flash('Error in login')
            return redirect(url_for('sign_up'))
        else:
            session['user_id'] = username_password_check.user_id

            # valid login credentials redirects user to home page
            flash('You were successfully logged in')

            # Redirects the user to their profile page upon login
            return redirect(url_for('user_profile', user_id=session['user_id']))


@app.route('/logout')
def logout():

    # remove the user_id from the session if it exists
    flash('You were successfully logged out')
    session.pop('user_id', None)
    return redirect(url_for('sign_up'))

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
