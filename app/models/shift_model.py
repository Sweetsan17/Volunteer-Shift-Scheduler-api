from datetime import datetime, timedelta

from app.extensions import db
from app.utils import utc_now


class Shift(db.Model):
    __tablename__ = "shifts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    shift_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    role_description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    event = db.relationship("Event", back_populates="shifts")
    signups = db.relationship(
        "Signup", back_populates="shift", cascade="all, delete-orphan", lazy="dynamic"
    )

    def duration_hours(self):
        start = datetime.combine(self.shift_date, self.start_time)
        end = datetime.combine(self.shift_date, self.end_time)
        if end <= start:
            end += timedelta(days=1)
        return round((end - start).total_seconds() / 3600, 2)

    def spots_taken(self):
        return self.signups.filter_by(status="confirmed").count()

    def is_full(self):
        return self.spots_taken() >= self.capacity

    def to_dict(self, include_event=False):
        data = {
            "id": self.id,
            "event_id": self.event_id,
            "shift_date": self.shift_date.isoformat(),
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "capacity": self.capacity,
            "role_description": self.role_description,
            "spots_taken": self.spots_taken(),
            "is_full": self.is_full(),
            "duration_hours": self.duration_hours(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_event and self.event:
            data["event"] = {
                "id": self.event.id,
                "title": self.event.title,
                "location": self.event.location,
            }
        return data
