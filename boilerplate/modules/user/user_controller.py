from boilerplate.app import app
import boilerplate.config as config
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role.role_actions import register_action
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from boilerplate.modules.role.role_decorators import require_action
from boilerplate.modules.user.user_model import User, send_password_reset, get_by_uuid, check_password_requirements
from boilerplate.utils.email import validate_address
from boilerplate.utils.urls import validate_uuid
from sqlalchemy.sql import func
import uuid

# ==============================================================================================================================================================
#                                                                      View Routes
# ==============================================================================================================================================================

# Page shows all users in the system
@app.get('/users')
@login_required
@require_action("read_users_list")
def get_user_list():
    roles = []
    if current_user.can("create_or_edit_user"):
        roles = Role.query.all()
    active_users = User.query.filter_by(active=True).all()
    deactivated_users = []
    if current_user.can("manage_deactivated_users"):
        deactivated_users = User.query.filter_by(active=False).all()
    return render_template("user/user_list.html",
                           active_users=active_users,
                           deactivated_users=deactivated_users,
                           roles=roles,
                           PASSWORD_MIN_CHARACTERS=config.PASSWORD_MIN_CHARACTERS,
                           PASSWORD_MAX_CHARACTERS=config.PASSWORD_MAX_CHARACTERS,
                           PASSWORD_REQUIRE_LOWER_CASE=config.PASSWORD_REQUIRE_LOWER_CASE,
                           PASSWORD_REQUIRE_UPPER_CASE=config.PASSWORD_REQUIRE_UPPER_CASE,
                           PASSWORD_REQUIRE_NUMERALS=config.PASSWORD_REQUIRE_NUMERALS,
                           PASSWORD_REQUIRE_SPECIAL_CHARACTERS=config.PASSWORD_REQUIRE_SPECIAL_CHARACTERS,
                           PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS=config.PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS
                            )

@app.get('/users/<profile_uuid>')
@login_required
def get_user_profile(profile_uuid: str):
    if not validate_uuid(profile_uuid):
        abort(400)
    user_uuid = uuid.UUID(profile_uuid)
    user = User.query.filter_by(uuid=user_uuid).first()
    if not user:
        abort(404)
    roles = Role.query.all()
    return render_template("user/profile.html", user=user, roles=roles)

@app.get('/password-reset')
def get_password_reset_screen():
    user_uuid = request.args.get("uuid")
    reset_code = request.args.get("reset-code")
    # Ensure all parameters are present
    if not (user_uuid or reset_code):
        return abort(400)

    # Lookup the correct user and ensure they exist
    user = get_by_uuid(user_uuid)
    if not user:
        return abort(403)

    # Validate the users reset code
    if not user.validate_reset_code(reset_code):
        return abort(403, description=f"This password reset link is no longer valid. "
                                           f"Password reset links are only valid for a period of {config.PASSWORD_RESET_CODE_VALIDITY} Minutes.")

    # Show the login screen
    return render_template("user/password-reset.html",
                           reset_code=reset_code,
                           user_uuid=user_uuid,
                           PASSWORD_MIN_CHARACTERS=config.PASSWORD_MIN_CHARACTERS,
                           PASSWORD_MAX_CHARACTERS=config.PASSWORD_MAX_CHARACTERS,
                           PASSWORD_REQUIRE_LOWER_CASE=config.PASSWORD_REQUIRE_LOWER_CASE,
                           PASSWORD_REQUIRE_UPPER_CASE=config.PASSWORD_REQUIRE_UPPER_CASE,
                           PASSWORD_REQUIRE_NUMERALS=config.PASSWORD_REQUIRE_NUMERALS,
                           PASSWORD_REQUIRE_SPECIAL_CHARACTERS=config.PASSWORD_REQUIRE_SPECIAL_CHARACTERS,
                           PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS=config.PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS
                            )

@app.post('/password-reset')
def post_complete_password_reset():
    user_uuid = request.form.get("uuid")
    reset_code = request.form.get("reset-code")
    password = request.form.get("password")
    password_confirm = request.form.get("password-confirm")
    # Ensure all parameters are present
    if not (user_uuid or reset_code or password or password_confirm):
        return abort(400)

    # Lookup the correct user and ensure they exist
    user = get_by_uuid(user_uuid)
    if not user:
        return abort(403)

    # Validate the users reset code
    if not user.validate_reset_code(reset_code):
        return abort(403, description=f"This password reset link is no longer valid. "
                                           f"Password reset links are only valid for a period of {config.PASSWORD_RESET_CODE_VALIDITY} Minutes.")


    password_rules_broken = check_password_requirements(password)
    if len(password_rules_broken) > 0:
        flash(f"Please ensure your password meets the following rules: {render_template('components/list.html', list=password_rules_broken)}", "error")
        return redirect(f"{url_for('get_password_reset_screen')}?uuid={user_uuid}&reset-code={reset_code}")

    if password != password_confirm:
        flash("Your passwords must match!", "error")
        return redirect(f"{url_for('get_password_reset_screen')}?uuid={user_uuid}&reset-code={reset_code}")
    user.update_password(password)

    # Show the login screen
    flash("Your password has been successfully updated.", "success")
    return redirect(url_for("get_login_page"))

# API route to perform a password reset Note: might want to rate limit this.
@app.post('/send-password-reset')
def post_send_password_reset():
    email_address = request.form.get("email")
    if email_address and validate_address(email_address):
        result = send_password_reset(email_address)
        if result == "error":
            flash("Could not reset password due to a system error. Please contact support to resolve this issue.", "error")
            return redirect(url_for("get_login_page"))
        # Always returning a success even if the user isn't present or sending is rate limited to avoid being able to
        # identify if an email is in the system or not.
        flash("If you have an account registered in the system you should receive an email shortly with instructions to reset your password.", "success")
        return redirect(url_for("get_login_page"))
    flash("Could not reset password. Please contact support to resolve this issue.", "error")
    return redirect(url_for("get_login_page"))


# ==============================================================================================================================================================
#                                                                 Action Registrations
# ==============================================================================================================================================================
register_action("read_users_list", "users", "Allows a user to see the list of users in a system.")
register_action("create_or_edit_user", "users", "Allows a user create or edit a user.", ("read_users_list",))
register_action("deactivate_user", "users", "Allows a user to deactivate a user account.", ("read_users_list",))
register_action("manage_deactivated_users", "users", "Allows a user to see, edit and activate deactivated users.", ("read_users_list","deactivate_user",))
