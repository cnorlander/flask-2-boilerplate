from boilerplate.app import app
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role import get_actions

@app.get('/api/v1/roles')
def get_roles_list():
    return Role.query.all()

@app.get('/api/v1/actions')
def get_actions_list():
    return get_actions()
