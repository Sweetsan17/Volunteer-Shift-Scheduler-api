from app.extensions import db
from app.utils import utc_now


class volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    volunteer_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "volunteer_id":self.volunteer_id,
            "full_name": self.full_name,
            "email": self.email,
            "age": self.age,
            "is_active": self.is_active,
            
        }