from flask import Blueprint, jsonify, Response

from CI_CD_server.src.services.build_service import (
    get_all_builds,
    get_build,
    get_builds_by_status,
)

build_bp = Blueprint("build", __name__)


@build_bp.route("/", methods=["GET"])
def list_all_builds() -> Response:
    """
    Retrieve a list of all builds, ordered by build date in descending order.

    Returns:
        jsonify: A JSON response containing a list of build dictionaries,
                 where each dictionary represents a build with its id, commit_sha,
                 build_date, and status.

    Example:
        >>> import requests
        >>> response = requests.get("http://localhost:5000/builds")
        >>> print(response.json())
        [{'id': 1, 'commit_sha': 'abcdef123456', 'build_date': '2025-02-12 10:30:00', 'status': 'success'}, {'id': 2, 'commit_sha': 'fedcba654321', 'build_date': '2025-02-11 15:45:00', 'status': 'failure'}]
    """
    builds = get_all_builds()
    return jsonify(builds)


@build_bp.route("/<int:build_id>", methods=["GET"])
def get_build_by_id(build_id: int) -> Response:
    """
    Retrieve a specific build by its ID.

    Args:
        build_id (int): The ID of the build to retrieve.

    Returns:
        jsonify: A JSON response containing a dictionary representing the build
                 with its id, commit_sha, build_date and status.
                 If the build is not found, returns a 404 error with a message.
    Example:
        >>> import requests
        >>> response = requests.get("http://localhost:5000/builds/1")
        >>> print(response.json())
        {'id': 1, 'commit_sha': 'abcdef123456', 'build_date': '2025-02-12 10:30:00', 'status': 'success'}

        >>> response = requests.get("http://localhost:5000/builds/999")
        >>> print(response.json())
        {'message': 'Build not found'}
    """
    build = get_build(build_id)
    if build:
        return jsonify(build)
    return jsonify({"message": "Build not found"}), 404


@build_bp.route("/errors", methods=["GET"])
def get_build_errors() -> Response:
    """
    Retrieve all builds with a "failure" status.

    Returns:
        jsonify: A JSON response containing a list of build dictionaries,
                 where each dictionary represents a build with a "failure" status.
                 If no builds with "failure" status are found, returns an empty list.

    Example:
        >>> import requests
        >>> response = requests.get("http://localhost:5000/builds/errors")
        >>> print(response.json())
        [{'id': 2, 'commit_sha': 'fedcba654321', 'build_date': '2025-02-11 15:45:00', 'status': 'failure', 'logs': '...'}]
    """
    builds = get_builds_by_status("failure")
    return jsonify(builds)


@build_bp.route("/successes", methods=["GET"])
def get_build_successes() -> Response:
    """
    Retrieve all builds with a "success" status.

    Returns:
        jsonify: A JSON response containing a list of build dictionaries,
                 where each dictionary represents a build with a "success" status.
                 If no builds with "success" status are found, returns an empty list.

    Example:
        >>> import requests
        >>> response = requests.get("http://localhost:5000/builds/successes")
        >>> print(response.json())
        [{'id': 1, 'commit_sha': 'abcdef123456', 'build_date': '2025-02-12 10:30:00', 'status': 'success', 'logs': '...'}]
    """
    builds = get_builds_by_status("success")
    return jsonify(builds)
