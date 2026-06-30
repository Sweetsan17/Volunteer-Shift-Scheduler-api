from flask import Flask

from app.config import Config
from app.extensions import db, bcrypt, jwt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

   
    from app.models import User, Event, Volunteer  

    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.volunteer_routes import volunteer_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(event_bp, url_prefix="/api/events")
    app.register_blueprint(volunteer_bp, url_prefix="/api/volunteers")

    with app.app_context():
        db.create_all()

    @app.get("/")
    def health_check():
        return {"status": "ok", "service": "volunteer-shift-scheduler-api"}

    return app