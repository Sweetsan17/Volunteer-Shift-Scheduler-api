from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user_model import User

ALLOWED_ROLES = {"admin", "coordinator", "volunteer"}


def register_user(data):
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "volunteer")

    if not email or not password:
        return {"error": "email and password are required"}, 400

    if role not in ALLOWED_ROLES:
        return {"error": "role must be one of: admin, coordinator, volunteer"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "A user with that email already exists"}, 409

    user = User(email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "User registered", "user": user.to_dict()}, 201


def login_user(data):
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    return {
        "message": "Login successful",
        "access_token": token,
        "user": user.to_dict(),
    }, 200
