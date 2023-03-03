from boilerplate.app import app
from boilerplate.modules.role import register_action
from flask import render_template, request, flash
from boilerplate.modules.user.user_model import User, send_password_reset
from boilerplate.utils.email import validate_address

from sqlalchemy.sql import func

# Page shows all users in the system
@app.get('/users')
def get_user_list():
    all_users = User.query.all()
    return render_template("user/user_list.html", all_users=all_users)

# API Route to show all users
# TODO: Lock this down using the role engine when possible
@app.get('/api/v1/users/')
def get_user_list_json():
    all_users = User.query.all()
    return all_users

@app.get('/password-reset')
def get_complete_password_reset():
    return func.now()

# API route to perform a password reset Note: might want to rate limit this.
@app.post('/api/v1/users/password-reset')
def post_send_password_reset():
    email_address = request.json.get("email")
    if email_address and validate_address(email_address):
        result = send_password_reset(email_address)
        if result == "error":
            return {"status": "error"}
        # Always returning a success even if the user isn't present or sending is rate limited to avoid being able to
        # identify if an email is in the system or not.
        return {"status": "success"}
    return {"status": "error"}

register_action("read_users_list", "users", "Allows a user to see the list of users in a system.")
register_action("create_or_edit_user", "users", "Allows a user create or edit a user.", ("read_users_list",))
register_action("disable_user", "users", "Allows a user to disable a user.", ("read_users_list",))
register_action("create_system_admins", "users", "Allows a user create System Admins.", system_only=True)
