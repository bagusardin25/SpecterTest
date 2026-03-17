import os

from flask import Flask
from flask_cors import CORS

from app.config import config
from app.extensions import db


def create_app(config_name=None):
    """Application factory — creates and configures the Flask app."""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensions
    CORS(app)
    db.init_app(app)

    # Register blueprints
    from app.api.scan import scan_bp
    from app.api.simulation import simulation_bp
    from app.api.report import report_bp

    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(simulation_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")

    # Create database tables
    with app.app_context():
        from app.models import scan, agent, finding, route  # noqa: F401
        db.create_all()

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal server error"}, 500

    return app
