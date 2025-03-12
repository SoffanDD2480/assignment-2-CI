from datetime import datetime, timezone

from CI_CD_server.src.database.db import db


class Build(db.Model):
    """
    Represents a build in the database.

    This class models build records with commit identifiers, build output logs,
    timestamps, and status information. Each build is associated with a specific
    commit in the version control system.
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

    status = db.Column(
        db.String(20), nullable=False, doc="Build status (max length 20)."
    )

    def __init__(self, commit_sha: str, status: str) -> None:
        """
        Initialize a new Build object.

        Args:
            commit_sha (str): Commit SHA for the build.
            status (str): Build status.
        """
        self.commit_sha = commit_sha
        self.status = status

    @staticmethod
    def add_build(commit_sha: str, status: str) -> None:
        """
        Add a new build to the database.

        Args:
            commit_sha (str): Commit SHA for the build.
            status (str): Build status.

        Example:
            >>> Build.add_build("abcdef123456", "Build logs...", "success")
            Adding build to database.
        """
        print("Adding build to database.")
        new_build = Build(commit_sha, status)
        db.session.add(new_build)
        db.session.commit()
