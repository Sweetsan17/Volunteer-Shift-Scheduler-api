from app.extensions import db
from app.utils import utc_now


class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shift_id = db.Column(
        db.Integer, db.ForeignKey("shifts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    signed_up_at = db.Column(db.DateTime, default=utc_now)
    cancelled_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("shift_id", "user_id", name="uniq_active_signup"),
    )

    shift = db.relationship("Shift", back_populates="signups")
    user = db.relationship("User", backref=db.backref("signups", lazy="dynamic"))

    def to_dict(self, include_user=False, include_shift=False):
        data = {
            "id": self.id,
            "shift_id": self.shift_id,
            "user_id": self.user_id,
            "status": self.status,
            "signed_up_at": self.signed_up_at.isoformat() if self.signed_up_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
        }
        if include_user and self.user:
            data["user"] = self.user.to_dict()
        if include_shift and self.shift:
            data["shift"] = self.shift.to_dict(include_event=True)
        return data
