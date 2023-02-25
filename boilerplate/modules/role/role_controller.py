from boilerplate.app import app
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role import get_actions, register_action

@app.get('/api/v1/roles')
def get_roles_list():
    return Role.query.all()

@app.get('/api/v1/actions')
def get_actions_list():
    return get_actions()

register_action("read_roles_list", "roles", "Allows a user to see the list of roles in the system.")
register_action("create_or_edit_role", "roles", "Allows a user create or edit a user role", ("read_roles_list",))
register_action("wumbo", "roles", "Does wumbo?", ("read_roles_list",))