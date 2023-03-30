from boilerplate.app import app
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role.role_actions import get_actions, get_action_names, register_action
from boilerplate.modules.role.role_decorators import require_action
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required

# ==============================================================================================================================================================
#                                                                      View Routes
# ==============================================================================================================================================================
@app.get('/roles')
@login_required
def get_roles_list():
    roles = Role.query.all()
    actions = get_actions()
    return render_template("role/role_list.html", actions=actions, roles=roles)

# ==============================================================================================================================================================
#                                                                  Context Processors
# ==============================================================================================================================================================
@app.context_processor
def context_processor_role_has_action():
    def role_has_action(role: Role, action: str):
        return role.has_action(action)
    return dict(role_has_action=role_has_action)


# ==============================================================================================================================================================
#                                                                 Action Registrations
# ==============================================================================================================================================================
register_action("read_roles_list", "roles", "Allows a user to see the list of roles in the system.")
register_action("create_or_edit_role", "roles", "Allows a user create or edit a user role", ("read_roles_list",))
register_action("wumbo", "roles", "Does wumbo?", ("read_roles_list",))