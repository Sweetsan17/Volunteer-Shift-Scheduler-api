from datetime import datetime

from app.extensions import db
from app.models.volunteer_model import Volunteer


def _to_bool(value, default=True):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "y")


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    return value


def create_volunteer(data):
    try:
        volunteer = Volunteer(
            full_name=data["full_name"],
            email=data["email"],
            phone=data.get("phone"),
            age=int(data["age"]) if data.get("age") not in (None, "") else None,
            joined_date=_parse_date(data.get("joined_date")),
            is_active=_to_bool(data.get("is_active"), default=True),
        )
    except (KeyError, ValueError, TypeError) as exc:
        return {"error": f"Invalid volunteer data: {exc}"}, 400

    db.session.add(volunteer)
    db.session.commit()
    return {"message": "Volunteer created", "volunteer": volunteer.to_dict()}, 201


def list_volunteers():
    volunteers = Volunteer.query.order_by(Volunteer.id.desc()).all()
    return {"volunteers": [v.to_dict() for v in volunteers]}, 200


def get_volunteer(volunteer_id):
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {"error": "Volunteer not found"}, 404
    return {"volunteer": volunteer.to_dict()}, 200


def update_volunteer(volunteer_id, data):
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {"error": "Volunteer not found"}, 404

    try:
        if "full_name" in data:
            volunteer.full_name = data["full_name"]
        if "email" in data:
            volunteer.email = data["email"]
        if "phone" in data:
            volunteer.phone = data["phone"]
        if "age" in data:
            volunteer.age = int(data["age"]) if data["age"] not in (None, "") else None
        if "joined_date" in data:
            volunteer.joined_date = _parse_date(data["joined_date"])
        if "is_active" in data:
            volunteer.is_active = _to_bool(data["is_active"])
    except (ValueError, TypeError) as exc:
        return {"error": f"Invalid volunteer data: {exc}"}, 400

    db.session.commit()
    return {"message": "Volunteer updated", "volunteer": volunteer.to_dict()}, 200


def delete_volunteer(volunteer_id):
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return {"error": "Volunteer not found"}, 404

    db.session.delete(volunteer)
    db.session.commit()
    return {"message": "Volunteer deleted"}, 200
