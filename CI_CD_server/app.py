from flask import Flask

from src.config.app_config import Config
from src.routes.init import register_routes
from src.database.db import init_db


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class for the application.

    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    init_db(app)

    # Register all routes
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=False)
