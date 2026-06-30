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


def create_event():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_event_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        event = Event(
            event_name=data.get("event_name").strip(),
            duration=float(data.get("duration")).strip(),
            volunteer_role=data.get("volunteer_role").strip(),
            description=data.get("description").strip(),
            is_active=data.get("is_active", True),
        )
        db.session.add(event)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Event created successfully.",
                    "event": event.to_dict(),
                }
            ),
            201,
        )
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
