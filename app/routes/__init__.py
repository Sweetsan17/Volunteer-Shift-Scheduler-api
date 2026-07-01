def register_blueprints(app):
    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.volunteer_routes import volunteer_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(event_bp, url_prefix="/api/events")
    app.register_blueprint(volunteer_bp, url_prefix="/api/volunteers")
