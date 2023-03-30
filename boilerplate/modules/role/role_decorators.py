from flask_login import current_user
from flask import abort
from functools import wraps


# ==============================================================================================================================================================
#                                                                   Role Decotators
# ==============================================================================================================================================================
def require_action(action: str):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not current_user.can(action):
                return abort(403)
            return function(*args, **kwargs)
        return decorated_function
    return decorator


def require_system_role(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return abort(403)
        if not current_user.role.system:
            return abort(403)
        return function(*args, **kwargs)
    return decorated_function