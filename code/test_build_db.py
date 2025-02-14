import pytest

from flask import Flask
from datetime import datetime, timedelta, timezone
from build_db import db, Build, init_db


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for each test using an in-memory DB."""
    app = Flask(__name__)

    # non-persistent in-memory database for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app)
    yield app


@pytest.fixture
def client(app):
    """A test client for the Flask app."""
    return app.test_client()


def test_build_table_name():
    """Verify that the Build model has the correct table name."""
    assert Build.__tablename__ == "builds"


def test_add_build(app, capsys):
    """
    Test the add_build static method.

    Verifies that:
    - The build is added to the database.
    - The printed output contains the expected message.
    - The build_date is properly set.
    """
    commit_sha = "abcdef123456"
    logs = "Test build logs"
    status = "success"

    with app.app_context():
        Build.add_build(commit_sha, logs, status)

        captured = capsys.readouterr().out
        assert "Adding build to database." in captured

        build = Build.query.filter_by(commit_sha=commit_sha).first()
        assert build is not None
        assert build.logs == logs
        assert build.status == status
        assert isinstance(build.build_date, datetime)

        now = datetime.now().replace(tzinfo=None)  


def test_build_instance_creation(app):
    """
    Test that a Build instance can be created, added to the session,
    and properly queried.
    """
    commit_sha = "123456abcdef"
    logs = "Another test build"
    status = "failed"

    with app.app_context():
        new_build = Build(commit_sha, logs, status)
        db.session.add(new_build)
        db.session.commit()

        build = Build.query.filter_by(commit_sha=commit_sha).first()
        assert build is not None
        assert build.commit_sha == commit_sha
        assert build.logs == logs
        assert build.status == status


def test_persistence_after_db_shutdown(tmp_path):
    """
    Test that data persists after a simulated database shutdown/restart.

    This test uses a temporary file-based SQLite database to verify that data
    added in one app context remains available after reinitializing the app.
    """
    db_file = tmp_path / "builds.db"
    db_uri = f"sqlite:///{db_file}"

    app1 = Flask(__name__)
    app1.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app1)

    with app1.app_context():
        Build.add_build("persist_sha", "Persistent logs", "success")
        build = Build.query.filter_by(commit_sha="persist_sha").first()
        assert build is not None
        assert build.logs == "Persistent logs"
        assert build.status == "success"

    app2 = Flask(__name__)
    app2.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app2)

    with app2.app_context():
        build = Build.query.filter_by(commit_sha="persist_sha").first()

        assert build is not None
        assert build.logs == "Persistent logs"
        assert build.status == "success"
