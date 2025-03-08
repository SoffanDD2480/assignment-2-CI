from .webhook_routes import webhook_bp
from .build_routes import build_bp


def register_routes(app):
    """
    Register all blueprint routes with the app.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(webhook_bp)
    app.register_blueprint(build_bp, url_prefix="/builds")
