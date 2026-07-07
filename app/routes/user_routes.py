from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from app.controllers import signup_controller
from app.middleware import roles_required

user_bp = Blueprint("users", __name__)


@user_bp.get("/me/shifts")
@roles_required("volunteer")
def my_shifts():
    body, status = signup_controller.get_my_shifts(current_user.id)
    return jsonify(body), status


@user_bp.get("/me/hours")
@jwt_required()
def my_hours():
    user_id = current_user.id
    if current_user.role in ("admin", "organizer"):
        requested = request.args.get("user_id")
        if requested:
            user_id = int(requested)
    elif current_user.role != "volunteer":
        return jsonify({"error": "Access forbidden: insufficient permissions."}), 403

    body, status = signup_controller.get_hours_volunteered(user_id)
    return jsonify(body), status
