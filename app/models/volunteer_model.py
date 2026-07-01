from app.extensions import db
from app.models.user_model import User


class Volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    joined_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)

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
