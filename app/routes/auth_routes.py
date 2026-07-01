from flask import Blueprint, jsonify, request

from app.controllers import auth_controller

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    body, status = auth_controller.register_user(request.get_json(force=True) or {})
    return jsonify(body), status


@auth_bp.post("/login")
def login():
    body, status = auth_controller.login_user(request.get_json(force=True) or {})
    return jsonify(body), status
