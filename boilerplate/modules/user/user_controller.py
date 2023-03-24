from boilerplate.app import app
import boilerplate.config as config
from boilerplate.modules.role import register_action
from flask import render_template, request, flash, redirect, url_for, abort
from boilerplate.modules.user.user_model import User, send_password_reset
from boilerplate.utils.email import validate_address

from sqlalchemy.sql import func

# Page shows all users in the system
@app.get('/users')
def get_user_list():
    all_users = User.query.all()
    return render_template("user/user_list.html", all_users=all_users)


@app.get('/password-reset')
def get_password_reset_screen():
    user_uuid = request.args.get("uuid")
    reset_code = request.args.get("reset-code")
    # Ensure all parameters are present
    if not (user_uuid or reset_code):
        return abort(400)

    # Lookup the correct user and ensure they exist
    user = User.get_by_uuid(user_uuid)
    if not user:
        return abort(403)

    # Validate the users reset code
    if not user.validate_reset_code(reset_code):
        return abort(403, detailed_message=f"This password reset link is no longer valid. "
                                           f"Password reset links are only valid for a period of {config.RESET_CODE_VALIDITY} Minutes.")

    # Show the login screen
    return render_template("user/password-reset.html")

@app.post('/password-reset')
def post_complete_password_reset():
    user_uuid = request.form.get("uuid")
    reset_code = request.form.get("reset-code")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")

    # Ensure all parameters are present
    if not (user_uuid or reset_code or password or password_confirm):
        return abort(400)

    # Lookup the correct user and ensure they exist
    user = User.get_by_uuid(user_uuid)
    if not user:
        return abort(403)

    # Validate the users reset code
    if not user.validate_reset_code(reset_code):
        return abort(403, detailed_message=f"This password reset link is no longer valid. "
                                           f"Password reset links are only valid for a period of {config.RESET_CODE_VALIDITY} Minutes.")

    # Update the password
    user.update_password(password)

    # Show the login screen
    return render_template("user/password-reset.html")

# API route to perform a password reset Note: might want to rate limit this.
@app.post('/send-password-reset')
def post_send_password_reset():
    email_address = request.form.get("email")
    if email_address and validate_address(email_address):
        result = send_password_reset(email_address)
        if result == "error":
            flash("An error has occured when trying to perform the password reset")
            return redirect(url_for("get_login_page"))
        # Always returning a success even if the user isn't present or sending is rate limited to avoid being able to
        # identify if an email is in the system or not.
        return {"status": "success"}
    return {"status": "error"}

register_action("read_users_list", "users", "Allows a user to see the list of users in a system.")
register_action("create_or_edit_user", "users", "Allows a user create or edit a user.", ("read_users_list",))
register_action("disable_user", "users", "Allows a user to disable a user.", ("read_users_list",))
register_action("create_system_admins", "users", "Allows a user create System Admins.", system_only=True)
