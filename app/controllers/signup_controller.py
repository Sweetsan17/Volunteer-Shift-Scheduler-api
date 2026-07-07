from datetime import date

from app.extensions import db
from app.models.shift_model import Shift
from app.models.signup_model import Signup
from app.utils import utc_now


def sign_up_for_shift(shift_id, user_id):
    shift = Shift.query.with_for_update().get(shift_id)
    if not shift:
        db.session.rollback()
        return {"error": "Shift not found"}, 404

    existing = Signup.query.filter_by(shift_id=shift_id, user_id=user_id).first()
    if existing and existing.status != "cancelled":
        db.session.rollback()
        return {"error": "Already signed up for this shift"}, 409

    confirmed_count = Signup.query.filter_by(
        shift_id=shift_id, status="confirmed"
    ).count()

    if confirmed_count >= shift.capacity:
        if existing:
            existing.status = "waitlisted"
            existing.signed_up_at = utc_now()
            existing.cancelled_at = None
            signup = existing
        else:
            signup = Signup(shift_id=shift_id, user_id=user_id, status="waitlisted")
            db.session.add(signup)
        db.session.commit()
        return {
            "message": "Shift is full — added to waitlist",
            "status": "waitlisted",
            "signup": signup.to_dict(),
        }, 201

    if existing:
        existing.status = "confirmed"
        existing.signed_up_at = utc_now()
        existing.cancelled_at = None
        signup = existing
    else:
        signup = Signup(shift_id=shift_id, user_id=user_id, status="confirmed")
        db.session.add(signup)
    db.session.commit()
    return {
        "message": "Signed up",
        "status": "confirmed",
        "signup": signup.to_dict(),
    }, 201


def cancel_signup(shift_id, user_id):
    signup = (
        Signup.query.filter_by(
            shift_id=shift_id, user_id=user_id, status="confirmed"
        )
        .with_for_update()
        .first()
    )
    if not signup:
        db.session.rollback()
        return {"error": "No active sign-up found"}, 404

    signup.status = "cancelled"
    signup.cancelled_at = utc_now()

    next_waiting = (
        Signup.query.filter_by(shift_id=shift_id, status="waitlisted")
        .order_by(Signup.signed_up_at.asc())
        .with_for_update()
        .first()
    )
    if next_waiting:
        next_waiting.status = "confirmed"

    db.session.commit()
    return {"message": "Sign-up cancelled"}, 200


def get_my_shifts(user_id):
    today = date.today()
    signups = (
        Signup.query.filter_by(user_id=user_id)
        .filter(Signup.status.in_(["confirmed", "waitlisted"]))
        .join(Shift)
        .order_by(Shift.shift_date, Shift.start_time)
        .all()
    )

    upcoming = []
    past = []
    for signup in signups:
        entry = signup.to_dict(include_shift=True)
        if signup.shift.shift_date >= today:
            upcoming.append(entry)
        else:
            past.append(entry)

    past.sort(key=lambda s: s["shift"]["shift_date"], reverse=True)
    return {"upcoming": upcoming, "past": past}, 200


def get_hours_volunteered(user_id):
    today = date.today()
    signups = (
        Signup.query.filter_by(user_id=user_id, status="confirmed")
        .join(Shift)
        .filter(Shift.shift_date < today)
        .all()
    )
    total_hours = sum(s.shift.duration_hours() for s in signups)
    return {"user_id": user_id, "hours_volunteered": round(total_hours, 2)}, 200
