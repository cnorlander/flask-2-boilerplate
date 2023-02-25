from boilerplate.app import app
from flask import Flask, render_template, redirect, request, flash, abort, url_for
from flask_login import LoginManager, login_user, logout_user
from boilerplate.modules.user.user_model import User, get_by_uuid
from boilerplate.utils.urls import is_safe_url
from boilerplate.db import db
from flask import render_template

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'get_login_page'

@login_manager.user_loader
def load_user(user_id: str):
    current_user = get_by_uuid(user_id)
    if (current_user is None) or (not current_user.active):
        flash("Your account with this service is no longer active. If you believe this to be in error please contact an admin and have your account reactivated")
        #return abort(403)
    return get_by_uuid(user_id)

@app.get("/login")
def get_login_page():
    return render_template("login/login_page.html")

@app.post("/login")
def post_login_user():
    # Get the login credentials from the form
    input_email = request.form.get("email")
    input_password = request.form.get("password")

    # Ensure all the required form data is present if not toss a HTTP 400 Error.
    # If your front end is working and validating no one should never see this error.
    if (not input_email) or (not input_password):
        #TODO: Flash a no data error
        return abort(400)

    # Get the user form the database.
    db_user = User.query.filter_by(email=input_email).first()
    print(db_user, flush=True)
    # If the user is not in the database toss flash a login error and return them to the login screen.
    if not db_user:
        flash("The credentials you supplied are incorrect. Please check your username and password and try again.")
        return redirect(url_for("get_login_page"))

    # Validate the users password is correct. If not toss a generic login error.
    if not db_user.validate_password(input_password):
        flash("The credentials you supplied are incorrect. Please check your username and password and try again.")
        return redirect(url_for("get_login_page"))

    # Ensure the users account is still active. If not toss a deactivated.
    if not db_user.active:
        flash(f"The account with email address \"{db_user.email}\" is deactivated and cannot login. If you believe this is in error please contact an admin.")
        return redirect(url_for("get_login_page"))

    # Log the user in!
    login_user(db_user)

    # Determine where the user intends to go next and if the origin is not the same as the request toss a 400.
    next_page = request.args.get('next')
    if not is_safe_url(next_page):
        return abort(400)

    # redirect the user where they wanted to go.
    return redirect(next_page or "/")



@app.get("/logout")
def get_logout():
    logout_user()
    return redirect(url_for("get_login_page"))
