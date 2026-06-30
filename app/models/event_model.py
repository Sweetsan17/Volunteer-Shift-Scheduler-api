from app.extensions import db
from app.models.volunteer_model import Volunteer
from app.utils import utc_now


class Event(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # volunteer_id = db.Column(db.Integer, ForeignKey=(Volunteer.volunteer_id))
    event_name = db.Column(db.String(100), nullable=False, unique=True)
    duration = db.Column(db.Float, nullable=False)
    volunteer_role = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "volunteer_id": self.volunteer_id,
            "event_name": self.event_name,
            "duration": self.duration,
            "volunteer_role": self.volunteer_role,
            "is_active": self.is_active,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
