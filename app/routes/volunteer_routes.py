from flask import Blueprint
from app.middleware import roles_required
from app.controllers import volunteer_controller as ctrl

volunteer_bp = Blueprint("volunteers", __name__, url_prefix=("/api/volunteers"))


@volunteer_bp.route("", methods=["POST"])
def create_volunteer():
    return ctrl.create_volunteer()


@volunteer_bp.route("", methods=["GET"])
def get_volunteers():
    return ctrl.get_volunteers()


@volunteer_bp.route("/<int:volunteer_id>", methods=["GET"])
def get_volunteer():
    return ctrl.get_volunteer()
