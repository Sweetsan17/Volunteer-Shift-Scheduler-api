from flask import Blueprint
from app.middleware import roles_required
from app.controllers import event_controller as ctrl

event_bp = Blueprint("events", __name__, url_prefix=("/api/events"))


@event_bp.route("", methods=["POST"])
def create_event():
    return ctrl.create_event()


@event_bp.route("", methods=["GET"])
def get_events():
    return ctrl.get_events()


@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    return ctrl.get_event(event_id)


@event_bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    return ctrl.update_event(event_id)
