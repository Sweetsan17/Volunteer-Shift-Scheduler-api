from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from app.controllers import shift_controller, signup_controller
from app.middleware import roles_required

shift_bp = Blueprint("shifts", __name__)


@shift_bp.get("")
@jwt_required()
def list_shifts():
    status_filter = request.args.get("status")
    body, status = shift_controller.list_shifts(status_filter)
    return jsonify(body), status


@shift_bp.get("/<int:shift_id>")
@jwt_required()
def get_shift(shift_id):
    body, status = shift_controller.get_shift(shift_id)
    return jsonify(body), status


@shift_bp.put("/<int:shift_id>")
@roles_required("admin", "organizer")
def update_shift(shift_id):
    body, status = shift_controller.update_shift(
        shift_id, request.get_json(force=True) or {}
    )
    return jsonify(body), status


@shift_bp.delete("/<int:shift_id>")
@roles_required("admin", "organizer")
def delete_shift(shift_id):
    body, status = shift_controller.delete_shift(shift_id)
    return jsonify(body), status


@shift_bp.get("/<int:shift_id>/roster")
@roles_required("admin", "organizer")
def get_roster(shift_id):
    body, status = shift_controller.get_roster(shift_id)
    return jsonify(body), status


@shift_bp.get("/<int:shift_id>/roster/export")
@roles_required("admin", "organizer")
def export_roster(shift_id):
    csv_content, meta, status = shift_controller.export_roster_csv(shift_id)
    if status != 200:
        return jsonify(meta), status
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={meta['filename']}"},
    )


@shift_bp.post("/<int:shift_id>/signup")
@roles_required("volunteer")
def sign_up(shift_id):
    body, status = signup_controller.sign_up_for_shift(shift_id, current_user.id)
    return jsonify(body), status


@shift_bp.delete("/<int:shift_id>/signup")
@roles_required("volunteer")
def cancel_signup(shift_id):
    body, status = signup_controller.cancel_signup(shift_id, current_user.id)
    return jsonify(body), status
