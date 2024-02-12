from flask import Blueprint, jsonify, request
from app.utilities.jwt.jwt_decorator import jwt_required
from flask import make_response

sample_app = Blueprint("sample", __name__)


@sample_app.route("/api/hello", methods=["GET"])
@jwt_required
def index_action(current_user):
    return (
        jsonify(),
        200,
    )
