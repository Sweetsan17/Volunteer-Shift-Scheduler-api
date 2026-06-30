from app.extensions import db
from app.utils import utc_now


class Event(db.Model):
    __tablename__ = "courses"

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_name = db.Column(db.String(100), nullable=False, unique=True)
    duration = db.Column(db.Interger, nullable=False)
    volunteer_role= db.Column(db.Text, nullable=True)
    volunteer_id = db.Column(db.Integer, default=True)
    is_available=db.Column(db.Boolean, default=True)
    description=db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def to_dict(self):
        return {
            "event_id": self.id,
            "event_name": self.event_name,
            "duration": self.duration,
            "volunteer_role": self.volunteer_role,
            "volunteer_id": self.volunteer_id,
            "is_available": self.is_available,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }