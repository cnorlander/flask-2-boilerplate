from boilerplate.app import app
from boilerplate.modules.role import register_action
from boilerplate.db import db
from flask import render_template
from boilerplate.modules.user.user_model import User

@app.get('/users')
def get_user_list():
    all_users = User.query.all()
    return render_template("user/user_list.html", all_users=all_users)

@app.get('/api/v1/users')
def get_user_list_json():
    all_users = User.query.all()
    return all_users

register_action("read_users_list", "users", "Allows a user to see the list of users in a system.")
register_action("create_or_edit_user", "users", "Allows a user create or edit a user.", ("read_users_list",))
register_action("disable_user", "users", "Allows a user to disable a user.", ("read_users_list",))
register_action("create_system_admins", "users", "Allows a user create System Admins.", system_only=True)
