from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.controllers import volunteer_controller
from app.middleware import roles_required

volunteer_bp = Blueprint("volunteers", __name__)


@volunteer_bp.post("")
@roles_required("admin", "coordinator")
def create_volunteer():
    body, status = volunteer_controller.create_volunteer(
        request.get_json(force=True) or {}
    )
    return jsonify(body), status


@volunteer_bp.get("")
@jwt_required()
def list_volunteers():
    body, status = volunteer_controller.list_volunteers()
    return jsonify(body), status


@volunteer_bp.get("/<int:volunteer_id>")
@jwt_required()
def get_volunteer(volunteer_id):
    body, status = volunteer_controller.get_volunteer(volunteer_id)
    return jsonify(body), status


@volunteer_bp.put("/<int:volunteer_id>")
@roles_required("admin", "coordinator")
def update_volunteer(volunteer_id):
    body, status = volunteer_controller.update_volunteer(
        volunteer_id, request.get_json(force=True) or {}
    )
    return jsonify(body), status


@volunteer_bp.delete("/<int:volunteer_id>")
@roles_required("admin", "coordinator")
def delete_volunteer(volunteer_id):
    body, status = volunteer_controller.delete_volunteer(volunteer_id)
    return jsonify(body), status
