from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from flask import jsonify
from functools import wraps


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user = get_jwt()["user"]
        except Exception as e:
            return jsonify(message="Missing or invalid token"), 401
        return fn(*args, **kwargs, current_user=user)

    return wrapper
