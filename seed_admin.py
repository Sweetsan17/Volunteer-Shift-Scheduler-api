"""
seed_admin.py
=============
This is a beginner-friendly script that creates ONE admin account.

Why do we need this file?
--------------------------
On the website, the public "Register" page only lets people sign up as
"volunteer" or "organizer" (see app/controllers/auth_controller.py).
Nobody can pick "admin" there. That is on purpose, so random visitors
can't make themselves an admin.

So how do we ever get an admin account? We run THIS script one time.
It creates a single admin user with a fixed name/email/password. If you
run it again, it will not create a duplicate — it just tells you the
admin already exists.

How to run it
--------------
    python seed_admin.py

The admin login will be:
    email:    admin@gmail.com
    password: admin123
"""

from app import create_app
from app.extensions import db
from app.models.user_model import User

# Change these values if you want a different admin account.
ADMIN_NAME = "admin"
ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"

app = create_app()

with app.app_context():
    # Step 1: check if this admin already exists, so we don't create it twice.
    existing_admin = User.query.filter_by(email=ADMIN_EMAIL).first()

    if existing_admin:
        print(f"Admin already exists: {ADMIN_EMAIL} (nothing to do).")
    else:
        # Step 2: create a new User row with role="admin".
        admin_user = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            role="admin",
        )
        # set_password() hashes the password before saving it —
        # we never store the plain text password in the database.
        admin_user.set_password(ADMIN_PASSWORD)

        # Step 3: save it to the database.
        db.session.add(admin_user)
        db.session.commit()

        print("Admin account created successfully!")
        print(f"  email:    {ADMIN_EMAIL}")
        print(f"  password: {ADMIN_PASSWORD}")
