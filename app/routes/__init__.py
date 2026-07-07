def register_blueprints(app):
    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.shift_routes import shift_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(event_bp, url_prefix="/api/events")
    app.register_blueprint(shift_bp, url_prefix="/api/shifts")
    app.register_blueprint(user_bp, url_prefix="/api/users")
