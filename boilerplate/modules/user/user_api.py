from boilerplate.app import app
from boilerplate.modules.user.user_model import User, get_user_by_uuid
from boilerplate.utils.urls import validate_uuid
from flask import abort
from flask_login import login_required
from boilerplate.modules.role.role_decorators import require_system_role

# ==============================================================================================================================================================
#                                                                   Endpoint Routes
# ==============================================================================================================================================================

# API Route to show all users
@app.get('/api/v1/users/')
@login_required
@require_system_role
def get_user_list_json():
    all_users = User.query.all()
    return all_users

@app.get('/api/v1/users/<profile_uuid>')
@login_required
@require_system_role
def get_user_profile_json(profile_uuid: str):
    if not validate_uuid(profile_uuid):
        abort(400)
    user = get_user_by_uuid(profile_uuid)
    if not user:
        abort(404)
    return user.dict()
