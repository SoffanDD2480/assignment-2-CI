from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Create an SQLAlchemy instance that will be used by the Flask app.
db = SQLAlchemy()


class Build(db.Model):
    """
    Represents a build in the database.
    """

    __tablename__ = "builds"

    id = db.Column(
        db.Integer, primary_key=True, doc="Primary key, auto-incrementing integer."
    )
    commit_sha = db.Column(
        db.String(100), nullable=False, doc="Commit SHA for the build (max length 100)."
    )

    build_date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        doc="Date and time of the build.",
    )

    logs = db.Column(db.Text, nullable=False, doc="Build logs (text).")
    status = db.Column(
        db.String(20), nullable=False, doc="Build status (max length 20)."
    )

    def __init__(self, commit_sha, logs, status):
        """
        Initialize a new Build object.

        Args:
            commit_sha (str): Commit SHA for the build.
            logs (str): Build logs.
            status (str): Build status.
        """
        self.commit_sha = commit_sha
        self.logs = logs
        self.status = status

    @staticmethod
    def add_build(commit_sha, logs, status):
        """
        Add a new build to the database.

        Args:
            commit_sha (str): Commit SHA for the build.
            logs (str): Build logs.
            status (str): Build status.

        Example:
            >>> Build.add_build("abcdef123456", "Build logs...", "success")
            Adding build to database.
        """
        print("Adding build to database.")
        new_build = Build(commit_sha, logs, status)
        db.session.add(new_build)
        db.session.commit()


def init_db(app):
    """
    Initialize the database for the Flask app.

    Args:
        app (Flask): The Flask application instance.

    Example:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> init_db(app)
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///builds.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
# test again final - 2