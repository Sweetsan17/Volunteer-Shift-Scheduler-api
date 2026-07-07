import csv
import io
from datetime import date, datetime, time

from app.extensions import db
from app.models.event_model import Event
from app.models.shift_model import Shift
from app.models.signup_model import Signup


def _parse_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def _parse_time(value):
    if isinstance(value, time):
        return value
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Invalid time format: {value}")


def create_shift(event_id, data):
    event = Event.query.get(event_id)
    if not event:
        return {"error": "Event not found"}, 404

    try:
        shift = Shift(
            event_id=event_id,
            shift_date=_parse_date(data["shift_date"]),
            start_time=_parse_time(data["start_time"]),
            end_time=_parse_time(data["end_time"]),
            capacity=int(data["capacity"]),
            role_description=data.get("role_description"),
        )
    except (KeyError, ValueError, TypeError) as exc:
        return {"error": f"Invalid shift data: {exc}"}, 400

    if shift.capacity < 1:
        return {"error": "capacity must be at least 1"}, 400

    db.session.add(shift)
    db.session.commit()
    return {"message": "Shift created", "shift": shift.to_dict()}, 201


def list_shifts(status_filter=None):
    query = Shift.query.order_by(Shift.shift_date, Shift.start_time)
    shifts = query.all()

    if status_filter == "open":
        shifts = [s for s in shifts if not s.is_full() and s.shift_date >= date.today()]

    return {"shifts": [s.to_dict(include_event=True) for s in shifts]}, 200


def get_shift(shift_id):
    shift = Shift.query.get(shift_id)
    if not shift:
        return {"error": "Shift not found"}, 404
    return {"shift": shift.to_dict(include_event=True)}, 200


def update_shift(shift_id, data):
    shift = Shift.query.get(shift_id)
    if not shift:
        return {"error": "Shift not found"}, 404

    try:
        if "shift_date" in data:
            shift.shift_date = _parse_date(data["shift_date"])
        if "start_time" in data:
            shift.start_time = _parse_time(data["start_time"])
        if "end_time" in data:
            shift.end_time = _parse_time(data["end_time"])
        if "capacity" in data:
            shift.capacity = int(data["capacity"])
            if shift.capacity < 1:
                return {"error": "capacity must be at least 1"}, 400
        if "role_description" in data:
            shift.role_description = data["role_description"]
    except (ValueError, TypeError) as exc:
        return {"error": f"Invalid shift data: {exc}"}, 400

    db.session.commit()
    return {"message": "Shift updated", "shift": shift.to_dict()}, 200


def delete_shift(shift_id):
    shift = Shift.query.get(shift_id)
    if not shift:
        return {"error": "Shift not found"}, 404

    db.session.delete(shift)
    db.session.commit()
    return {"message": "Shift deleted"}, 200


def get_roster(shift_id):
    shift = Shift.query.get(shift_id)
    if not shift:
        return {"error": "Shift not found"}, 404

    signups = (
        Signup.query.filter_by(shift_id=shift_id)
        .filter(Signup.status.in_(["confirmed", "waitlisted"]))
        .order_by(Signup.signed_up_at)
        .all()
    )
    return {
        "shift": shift.to_dict(include_event=True),
        "roster": [s.to_dict(include_user=True) for s in signups],
    }, 200


def export_roster_csv(shift_id):
    shift = Shift.query.get(shift_id)
    if not shift:
        return None, {"error": "Shift not found"}, 404

    signups = (
        Signup.query.filter_by(shift_id=shift_id)
        .filter(Signup.status.in_(["confirmed", "waitlisted"]))
        .order_by(Signup.signed_up_at)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Email", "Status", "Signed Up At"])
    for signup in signups:
        writer.writerow([
            signup.user.name,
            signup.user.email,
            signup.status,
            signup.signed_up_at.isoformat() if signup.signed_up_at else "",
        ])

    filename = f"roster-shift-{shift_id}.csv"
    return output.getvalue(), {"filename": filename}, 200
