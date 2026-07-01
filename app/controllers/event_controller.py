from app.extensions import db
from app.models.event_model import Event


def _to_bool(value, default=True):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "y")


def create_event(data):
    try:
        event = Event(
            event_name=data["event_name"],
            volunteers_needed=int(data["volunteers_needed"]),
            duration_hours=float(data["duration_hours"]),
            description=data.get("description"),
            is_available=_to_bool(data.get("is_available"), default=True),
        )
    except (KeyError, ValueError, TypeError) as exc:
        return {"error": f"Invalid event data: {exc}"}, 400

    db.session.add(event)
    db.session.commit()
    return {"message": "Event created", "event": event.to_dict()}, 201


def list_events():
    events = Event.query.order_by(Event.id.desc()).all()
    return {"events": [e.to_dict() for e in events]}, 200


def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404
    return {"event": event.to_dict()}, 200


def update_event(event_id, data):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    try:
        if "event_name" in data:
            event.event_name = data["event_name"]
        if "volunteers_needed" in data:
            event.volunteers_needed = int(data["volunteers_needed"])
        if "duration_hours" in data:
            event.duration_hours = float(data["duration_hours"])
        if "description" in data:
            event.description = data["description"]
        if "is_available" in data:
            event.is_available = _to_bool(data["is_available"])
    except (ValueError, TypeError) as exc:
        return {"error": f"Invalid event data: {exc}"}, 400

    db.session.commit()
    return {"message": "Event updated", "event": event.to_dict()}, 200


def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}, 200
