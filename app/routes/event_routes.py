from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from app.controllers import event_controller, shift_controller
from app.middleware import roles_required

event_bp = Blueprint("events", __name__)


@event_bp.post("")
@roles_required("admin", "organizer")
def create_event():
    body, status = event_controller.create_event(
        request.get_json(force=True) or {}, current_user.id
    )
    return jsonify(body), status


@event_bp.get("")
@jwt_required()
def list_events():
    body, status = event_controller.list_events()
    return jsonify(body), status


@event_bp.get("/<int:event_id>")
@jwt_required()
def get_event(event_id):
    body, status = event_controller.get_event(event_id)
    return jsonify(body), status


@event_bp.put("/<int:event_id>")
@roles_required("admin", "organizer")
def update_event(event_id):
    body, status = event_controller.update_event(
        event_id, request.get_json(force=True) or {}
    )
    return jsonify(body), status


@event_bp.delete("/<int:event_id>")
@roles_required("admin", "organizer")
def delete_event(event_id):
    body, status = event_controller.delete_event(event_id)
    return jsonify(body), status


@event_bp.post("/<int:event_id>/shifts")
@roles_required("admin", "organizer")
def create_shift(event_id):
    body, status = shift_controller.create_shift(
        event_id, request.get_json(force=True) or {}
    )
    return jsonify(body), status
