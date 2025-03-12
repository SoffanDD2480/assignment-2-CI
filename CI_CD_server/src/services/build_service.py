from typing import Optional
from CI_CD_server.src.models.build import Build


def get_all_builds() -> list[dict]:
    """
    Retrieve all builds ordered by date (newest first).

    Returns:
        list: List of dictionaries containing build information
    """
    all_builds = Build.query.order_by(Build.build_date.desc()).all()
    return [format_build(build) for build in all_builds]


def get_build(build_id: int) -> Optional[dict]:
    """
    Retrieve a build by ID.

    Args:
        build_id (int): ID of the build to retrieve

    Returns:
        dict: Build information or None if not found
    """
    build = Build.query.get(build_id)
    if build:
        return format_build(build)
    return None


def get_builds_by_status(status: str) -> list[dict]:
    """
    Retrieve builds filtered by status.

    Args:
        status (str): Status to filter by ('success' or 'failure')

    Returns:
        list: List of dictionaries containing build information
    """
    builds = Build.query.filter_by(status=status).all()
    return [format_build(build) for build in builds]


def format_build(build: Build) -> dict:
    """
    Format a build object as a dictionary.

    Args:
        build (Build): Build object to format

    Returns:
        dict: Dictionary representation of the build
    """
    result = {
        "id": build.id,
        "commit_sha": build.commit_sha,
        "build_date": build.build_date,
        "status": build.status,
    }

    return result
