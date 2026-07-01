from app.routes.auth_routes import auth_bp
from app.routes.event_routes import event_bp
from app.routes.volunteer_routes import volunteer_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(volunteer_bp)
