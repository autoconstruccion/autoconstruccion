from flask_login import current_user
from functools import wraps
from flask import abort


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def is_manager(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_manager():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
