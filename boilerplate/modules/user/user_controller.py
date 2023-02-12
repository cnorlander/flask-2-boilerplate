from boilerplate.app import app
from boilerplate.db import db
from flask import render_template
from boilerplate.modules.user.user_model import User

@app.get('/users')
def user_list():
    all_users = User.query.all()
    return render_template("user/user_list.html", all_users=all_users)
