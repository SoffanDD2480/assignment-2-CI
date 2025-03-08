import os


class Config:
    """Base configuration.

    This class defines the default configuration settings for the CI/CD server.
    It includes database connection settings and repository configuration.
    """

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///builds.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Repository settings
    BASE_DIR = os.environ.get("BASE_DIR", "./.sample_dir/")
    REPO_NAME = os.environ.get("REPO_NAME", "assignment-2-CI")
    REPO_URL = os.environ.get(
        "REPO_URL", "https://github.com/SoffanDD2480/assignment-2-CI.git"
    )


class TestConfig(Config):
    """Test configuration.

    This class extends the base Config class and overrides settings
    specifically for testing environments.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
