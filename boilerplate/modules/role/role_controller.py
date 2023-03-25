from boilerplate.app import app
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role import get_actions, register_action
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required

@app.context_processor
def context_processor_role_has_action():
    def role_has_action(role: Role, action: str):
        return role.has_action(action)
    return dict(role_has_action=role_has_action)


@app.get('/roles')
def get_roles_list():
    roles = Role.query.all()
    actions = get_actions()
    print(actions, flush=True)
    return render_template("role/role_list.html", actions=actions, roles=roles)


register_action("read_roles_list", "roles", "Allows a user to see the list of roles in the system.")
register_action("create_or_edit_role", "roles", "Allows a user create or edit a user role", ("read_roles_list",))
register_action("wumbo", "roles", "Does wumbo?", ("read_roles_list",))