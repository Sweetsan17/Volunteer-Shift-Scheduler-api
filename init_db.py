"""
Initialize the database schema.

Run:  python init_db.py

This wipes and recreates every table (users, events, shifts, signups) —
handy while building/testing the project. It also creates the one admin
account so you don't have to run a second script. See seed_admin.py for
details on why admin accounts work this way.
"""
from app import create_app
from app.extensions import db
from app.models.user_model import User

ADMIN_NAME = "admin"
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created successfully.")

    admin_user = User(name=ADMIN_NAME, email=ADMIN_EMAIL, role="admin")
    admin_user.set_password(ADMIN_PASSWORD)
    db.session.add(admin_user)
    db.session.commit()

    print("Admin account created:")
    print(f"  email:    {ADMIN_EMAIL}")
    print(f"  password: {ADMIN_PASSWORD}")
