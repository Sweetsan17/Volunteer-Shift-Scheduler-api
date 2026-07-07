from app.extensions import db
from app.models.event_model import Event


def create_event(data, user_id):
    title = data.get("title", "").strip()
    if not title:
        return {"error": "title is required"}, 400

    event = Event(
        title=title,
        description=data.get("description"),
        location=data.get("location"),
        created_by=user_id,
    )

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
    return {"event": event.to_dict(include_shifts=True)}, 200


def update_event(event_id, data):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    if "title" in data:
        title = data["title"].strip()
        if not title:
            return {"error": "title cannot be empty"}, 400
        event.title = title
    if "description" in data:
        event.description = data["description"]
    if "location" in data:
        event.location = data["location"]

    db.session.commit()
    return {"message": "Event updated", "event": event.to_dict()}, 200


def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    db.session.delete(event)
    db.session.commit()
    return {"message": "Event deleted"}, 200
