from boilerplate.app import app
from boilerplate.db import db
import boilerplate.modules.user.user_model as user_model

@app.get('/users')
def user_list():
    return "Test!"