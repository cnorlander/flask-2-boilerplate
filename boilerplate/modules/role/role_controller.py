from boilerplate.app import app
from boilerplate.modules.role import get_actions

@app.get('/roles')
def get_role_list():
    return get_actions()
