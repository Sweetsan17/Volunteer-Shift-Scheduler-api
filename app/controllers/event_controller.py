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


def get_events():
    events = Event.query.all()
    return jsonify({"events": [s.to_dict() for s in events]}), 200


def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found."}), 404
    return jsonify({"event": event.to_dict()}), 200


def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_event_payload(data, event_id=event_id)
    if errors:
        return jsonify({"errors": errors}), 400
    try:
        event.full_name = data.get("full_name").strip()
        event.email = data.get("email").strip()
        event.age = int(data.get("age"))

        if "is_active" in data:
            event.is_active = bool(data.get("is_active"))

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Event updated successfully.",
                    "event": event.to_dict(),
                }
            ),
            200,
        )
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found."}), 404
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
