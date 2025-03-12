from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from CI_CD_server.src.config.server_logger_config import server_logger

# Create an SQLAlchemy instance that will be used across the application
db = SQLAlchemy()


def init_db(app: Flask) -> None:
    """
    Initialize the database for the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Example:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> init_db(app)
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///builds.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    server_logger.info("Database initialized.")
    with app.app_context():
        db.create_all()
