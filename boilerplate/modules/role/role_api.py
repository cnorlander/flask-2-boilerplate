from boilerplate.app import app
from boilerplate.modules.role.role_model import Role
from boilerplate.modules.role.role_actions import get_actions, register_action
from flask_login import current_user, login_required
from flask import abort


# ==============================================================================================================================================================
#                                                                   Endpoint Routes
# ==============================================================================================================================================================
@app.get('/api/v1/roles')
@login_required
def get_all_roles():
    if current_user.role.system:
        return Role.query.all()
    return abort(403)

@app.get('/api/v1/actions')
@login_required
def get_all_actions():
    if current_user.role.system:
        return get_actions()
    return abort(403)
