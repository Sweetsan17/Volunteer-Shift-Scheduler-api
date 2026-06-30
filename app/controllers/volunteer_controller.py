from flask import jsonify, request
from app.extensions import db
from app.models.volunteer_model import Volunteer


def _validate_volunteer_payload(data, volunteer_id=None):
    errors = []
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    full_name = data.get("full_name")
    if full_name is None or str(full_name).strip() == "":
        errors.append("full name is required.")

    email = data.get("email")
    if email is None or str(email).strip() == "":
        errors.append("email is required.")
    elif str(email).strip():
        q = volunteer_id.query.filter(Volunteer.email == str(email).strip())
        if volunteer_id:
            q = q.filter(Volunteer.id != volunteer_id)
        if q.first():
            errors.append("Email address already exists.")

    age = data.get("age")
    if age is None:
        errors.append("age is required.")
    else:
        try:
            age_val = int(age)
            if age_val <= 0:
                errors.append("age must be a positive integer.")
        except (TypeError, ValueError):
            errors.append("age must be a positive integer.")

    return errors


def create_volunteer():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_volunteer_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        volunteer = Volunteer(
            id=data.get("id").strip(),
            full_name=data.get("full_name").strip(),
            email=data.get("email").strip(),
            age=int(data.get("age")),
            is_active=data.get("is_active", True),
        )
        db.session.add(volunteer)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Volunteer created successfully.",
                    "volunteer": volunteer.to_dict(),
                }
            ),
            201,
        )
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
