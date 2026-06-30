from flask import Blueprint
from app.middleware import roles_required
from app.controllers import event_controller as ctrl

event_bp = Blueprint("events", __name__, url_prefix=("/api/events"))
