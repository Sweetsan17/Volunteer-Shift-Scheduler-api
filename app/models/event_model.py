from app.extensions import db
from app.utils import utc_now


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    creator = db.relationship("User", backref=db.backref("events", lazy="dynamic"))
    shifts = db.relationship(
        "Shift",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="dynamic",
        order_by="Shift.shift_date",
    )

    def to_dict(self, include_shifts=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_shifts:
            data["shifts"] = [s.to_dict() for s in self.shifts]
        return data
