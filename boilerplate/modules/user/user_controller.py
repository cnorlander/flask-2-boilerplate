from boilerplate.app import app
import boilerplate.config as config
from boilerplate.db import save
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role.role_actions import register_action
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from boilerplate.modules.role.role_model import get_role_by_uuid
from boilerplate.modules.role.role_decorators import require_action
from boilerplate.modules.user.user_model import User, send_password_reset, get_user_by_uuid, check_password_requirements, get_user_by_email, create_if_not_exists
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

@app.get('/users/<user_uuid>')
@login_required
def get_user_profile(user_uuid: str):
    if not validate_uuid(user_uuid):
        abort(400)
    user = get_user_by_uuid(user_uuid)
    is_users_profile = str(current_user.uuid) == user_uuid
    if not user:
        abort(404)
    roles = Role.query.all()
    return render_template("user/profile.html",
                           user=user,
                           roles=roles,
                           is_users_profile=is_users_profile,
                           PASSWORD_MIN_CHARACTERS=config.PASSWORD_MIN_CHARACTERS,
                           PASSWORD_MAX_CHARACTERS=config.PASSWORD_MAX_CHARACTERS,
                           PASSWORD_REQUIRE_LOWER_CASE=config.PASSWORD_REQUIRE_LOWER_CASE,
                           PASSWORD_REQUIRE_UPPER_CASE=config.PASSWORD_REQUIRE_UPPER_CASE,
                           PASSWORD_REQUIRE_NUMERALS=config.PASSWORD_REQUIRE_NUMERALS,
                           PASSWORD_REQUIRE_SPECIAL_CHARACTERS=config.PASSWORD_REQUIRE_SPECIAL_CHARACTERS,
                           PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS=config.PASSWORD_LIST_OF_ALLOWED_SPECIAL_CHARACTERS
                           )

@app.post('/users/<user_uuid>')
@login_required
@require_action("create_or_edit_user")
def post_update_user(user_uuid: str):
    user_first_name = request.form.get("first-name")
    user_last_name = request.form.get("last-name")
    user_email = request.form.get("email")
    user_role = request.form.get("role-id")
    user_password = request.form.get("password")
    if (not user_first_name) or (not user_last_name) or (not user_email) or (not user_role) \
            or (not validate_address(user_email)) or (not validate_uuid(user_uuid)):
        return abort(400)

    # Check for existing user
    existing_user = get_user_by_uuid(user_uuid)
    if not existing_user:
        return abort(404)

    # Make sure password rules are followed
    if user_password and len(user_password) > 0 and (current_user.uuid == existing_user.uuid or current_user.can("update_passwords")):
        password_rules_broken = check_password_requirements(user_password)
        if len(password_rules_broken) > 0:
            flash(f"Please ensure your password meets the following rules: {render_template('components/list.html', list=password_rules_broken)}", "error")
            return redirect(url_for("get_user_list"))
        existing_user.update_password(user_password)

    # Ensure the role exists and is active
    existing_role = get_role_by_uuid(user_role)
    if (not existing_role) or (not existing_role.active):
        flash(f"The role you selected for the new user could not be found, longer exists or is not active. Please try again.", "error")
        return redirect(url_for("get_user_profile", user_uuid=user_uuid))

    # Ensure the user is not giving someone a role they shouldn't be able to
    if (existing_role.hidden or existing_role.system) and not current_user.role.system:
        return abort(403)

    # Update the user
    existing_user.first_name = user_first_name
    existing_user.last_name = user_last_name
    existing_user.email = user_email
    existing_user.role = existing_role

    # If a DB error occured tell the user
    if not save():
        flash(f"A database error occured while creating the user. Please try again otherwise contact an admin.", "error")
        return redirect(url_for("get_user_profile", user_uuid=user_uuid))

    # Success!
    flash(f"User updated successfully!", "success")
    return redirect(url_for("get_user_profile", user_uuid=user_uuid))

@app.post('/users/create')
@login_required
@require_action("create_or_edit_user")
def post_create_user():
    user_first_name = request.form.get("first-name")
    user_last_name = request.form.get("last-name")
    user_email = request.form.get("email")
    user_role = request.form.get("role-id")
    user_password = request.form.get("password")
    if (not user_first_name) or (not user_last_name) or (not user_email) or (not user_role) or (not user_password) or (not validate_address(user_email)):
        return abort(400)

    # Check for existing user
    existing_user = get_user_by_email(user_email)
    if existing_user:
        error_string = f'A user with the email address "{user_email}" already exists. '
        if not existing_user.active:
            error_string = f'A user with the email address "{user_email}" already exists and is deactivated. '
            if not current_user.can("manage_deactivated_users"):
                error_string += 'You will need an admin or someone with the Manage Disabled Users permission to activate the account.'
        flash(error_string, "error")
        return redirect(url_for("get_user_list"))

    # Make sure password rules are followed
    password_rules_broken = check_password_requirements(user_password)
    if len(password_rules_broken) > 0:
        flash(f"Please ensure your password meets the following rules: {render_template('components/list.html', list=password_rules_broken)}", "error")
        return redirect(url_for("get_user_list"))

    # Ensure the role exists and is active
    existing_role = get_role_by_uuid(user_role)
    if (not existing_role) or (not existing_role.active):
        flash(f"The role you selected for the new user could not be found, longer exists or is not active. Please try again.", "error")
        return redirect(url_for("get_user_list"))

    # Ensure the user is not giving someone a role they shouldn't be able to
    if (existing_role.hidden or existing_role.system) and not current_user.role.system:
        return abort(403)

    # Create the user
    is_created = create_if_not_exists(User(user_email, user_first_name, user_last_name, user_password, existing_role))

    # If a DB error occured tell the user
    if not is_created:
        flash(f"A database error occured while creating the user. Please try again otherwise contact an admin.", "error")
        return redirect(url_for("get_user_list"))

    # Success!
    flash(f"User created successfully!", "success")
    return redirect(url_for("get_user_list"))


@app.get('/password-reset')
def get_password_reset_screen():
    user_uuid = request.args.get("uuid")
    reset_code = request.args.get("reset-code")
    # Ensure all parameters are present
    if not (user_uuid or reset_code):
        return abort(400)

    # Lookup the correct user and ensure they exist
    user = get_user_by_uuid(user_uuid)
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
    user = get_user_by_uuid(user_uuid)
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
register_action("update_passwords", "users", "Allows a user to update the password of other user account.", ("read_users_list", "create_or_edit_user",))
register_action("deactivate_user", "users", "Allows a user to deactivate a user account.", ("read_users_list",))
register_action("manage_deactivated_users", "users", "Allows a user to see, edit and activate deactivated users.", ("read_users_list","deactivate_user",))
