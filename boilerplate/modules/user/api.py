from boilerplate.app import app
from boilerplate.modules.user.user_model import User



# API Route to show all users
# TODO: Lock this down using the role engine when possible
@app.get('/api/v1/users/')
def get_user_list_json():
    all_users = User.query.all()
    return all_users
