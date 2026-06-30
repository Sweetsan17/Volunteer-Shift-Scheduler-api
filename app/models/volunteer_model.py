from datetime import datetime

from app.extensions import db


class Volunteer(db.Model):
    """A volunteer roster entry (managed by admins/coordinators)."""

    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    joined_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "age": self.age,
            "joined_date": self.joined_date.isoformat() if self.joined_date else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }