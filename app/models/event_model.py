from datetime import datetime

from app.extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(150), nullable=False)
    volunteers_needed = db.Column(db.Integer, nullable=False, default=0)
    duration_hours = db.Column(db.Float, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "event_name": self.event_name,
            "volunteers_needed": self.volunteers_needed,
            "duration_hours": self.duration_hours,
            "description": self.description,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }