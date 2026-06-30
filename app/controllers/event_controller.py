from flask import jsonify, request
from app.extensions import db
from app.models.event_model import Event


def _validate_event_payload(data, event_id=None):
    errors = []
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    event_name = data.get("event_name")
    if event_name is None or str(event_name).strip() == "":
        errors.append("event_name is required.")
    elif str(event_name).strip():
        q = event_id.query.filter(Event.event_name == str(event_name).strip())
        if event_id:
            q = q.filter(Event.id != event_id)
        if q.first():
            errors.append("Event Name already exists.")

    duration = data.get("duration")
    if duration is None or str(duration).strip() == "":
        errors.append("duration is required.")

    volunteer_role = data.get("volunteer_role")
    if volunteer_role is None or str(volunteer_role).strip() == "":
        errors.append("volunteer role is required.")

    return errors


