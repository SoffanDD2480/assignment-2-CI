import os
import logging
import re
import io

from flask import Flask, request, jsonify
from syntax_check import check_syntax_and_formatting
from email_response import Response
from git_helpers import clone_repo, filter_files
from tests import test_changed_code_files
from generate_docs import generate_docs
from build_db import db, Build, init_db

app = Flask(__name__)
init_db(app)

# Base directory and repository details.
BASE_DIR = "./.sample_dir/"
REPO_NAME = "assignment-2-CI"
REPO_URL = "https://github.com/SoffanDD2480/assignment-2-CI.git"
LOG_FILE = "server.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle GitHub webhook POST requests for push events.

    This endpoint processes GitHub push events by:

    1. Validating the webhook event type.
    2. Extracting push event data (branch, pusher info).
    3. Cloning the repository.
    4. Checking changed files.
    5. Running syntax checks and tests.
    6. Sending email notifications with results.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

        - **For non-push events**: `({"message": "Not a push event"}, 200)`
        - **For successful processing**: `({"status": "success", "message": "Webhook processed"}, 200)`
        - **For errors**: `({"status": "error", "message": "<error details>"}, 500)`

    Raises:
        Exception: Logs any errors during webhook processing.

    Example:
        To trigger the webhook with a push event, use:

        .. code-block:: bash

            curl -X POST http://localhost:5000/webhook \
                -H "Content-Type: application/json" \
                -H "X-Github-Event: push" \
                -d '{
                    "ref": "refs/heads/main",
                    "pusher": {
                        "name": "username",
                        "email": "user@example.com"
                    },
                    "commits": [{
                        "added": ["code/new_file.py"],
                        "modified": ["code/existing_file.py"],
                        "removed": []
                    }]
                }'

    """

    log_capture_string = io.StringIO()
    mem_handler = logging.StreamHandler(log_capture_string)
    mem_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    mem_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(mem_handler)

    overall_success = True  # Track overall success of the build.
    logging.info("Received webhook request.")
    # Process only push events.
    if request.headers.get("X-Github-Event") != "push":
        logging.info("Ignored event (not a push event).")
        return jsonify({"message": "Not a push event"}), 200

    try:
        data = request.get_json()
        current_branch = data.get("ref", "")
        current_branch = re.search(r"refs/heads/(.+)", current_branch).group(1)
        pusher_info = data.get("pusher", {})
        commit_sha = data.get("after", "unknown")
        pusher_name = pusher_info.get("name")
        pusher_email = pusher_info.get("email")
        email_response = Response((pusher_name, pusher_email), current_branch)

        logging.info(
            f"Processing push event from {pusher_name} ({pusher_email}) on branch {current_branch}."
        )
        # Clone the repository into BASE_DIR/REPO_NAME.
        repo_path = clone_repo(BASE_DIR, REPO_NAME, current_branch, REPO_URL)
        logging.info(f"Repository cloned to {repo_path}.")
        generate_docs(logging)
        logging.info("Docs generated.")

        changed_code_files = filter_files(data)

        if not changed_code_files:
            logging.info("No Python code changes detected.")
            email_response.append_content("No Python code changes detected.")
        else:
            for file_path in changed_code_files:
                local_code_file = os.path.join(repo_path, file_path)
                email_response.append_content(f"Processing changed file: {file_path}")
                logging.info(f"Processing changed file: {file_path}")

                # Check syntax and auto-format
                if not check_syntax_and_formatting(
                    local_code_file, file_path, email_response, logging
                ):
                    # If syntax fails, skip tests for this file.
                    overall_success = False
                    continue

                # Run the tests.
                test_changed_code_files(
                    changed_code_files, repo_path, email_response, logging
                )

        logging.info(f"Webhook processed for branch: {current_branch}" + "\n")
        # Build and send (or print) the email response.
        email_response.make_response()
        if not app.debug:
            email_response.send_response()
            logging.info(f"Sent email contents: {email_response.body}")
        else:
            print("Debug mode: Email would have been sent with content:")
            print(email_response.body)
            print("END OF EMAIL CONTENT\n")
            logging.info(
                f"Debug mode: Email content that would have been sent: {email_response.body}."
            )

        build_status = "success" if overall_success else "failure"

        # get logs
        mem_handler.flush()
        build_logs = log_capture_string.getvalue()

        Build.add_build(commit_sha, build_logs, build_status)

        logging.info("Webhook processed.")
        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/builds", methods=["GET"])
def list_all_builds():
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
    all_builds = Build.query.order_by(Build.build_date.desc()).all()
    builds = [
        {
            "id": build.id,
            "commit_sha": build.commit_sha,
            "build_date": build.build_date,
            "status": build.status,
        }
        for build in all_builds
    ]
    return jsonify(builds)


@app.route("/builds/<int:build_id>", methods=["GET"])
def get_build_by_id(build_id):
    """
    Retrieve a specific build by its ID.

    Args:
        build_id (int): The ID of the build to retrieve.

    Returns:
        jsonify: A JSON response containing a dictionary representing the build
                 with its id, commit_sha, build_date, status, and logs.
                 If the build is not found, returns a 404 error with a message.
    Example:
        >>> import requests
        >>> response = requests.get("http://localhost:5000/builds/1")
        >>> print(response.json())
        {'id': 1, 'commit_sha': 'abcdef123456', 'build_date': '2025-02-12 10:30:00', 'status': 'success', 'logs': '...'}

        >>> response = requests.get("http://localhost:5000/builds/999")
        >>> print(response.json())
        {'message': 'Build not found'}
    """
    build = Build.query.get(build_id)
    build = [
        {
            "id": build.id,
            "commit_sha": build.commit_sha,
            "build_date": build.build_date,
            "status": build.status,
            "logs": build.logs,
        }
    ]
    if build:
        return jsonify(build)
    return jsonify({"message": "Build not found"}), 404


@app.route("/builds/errors", methods=["GET"])
def get_build_errors():
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
    all_builds = Build.query.filter_by(status="failure").all()
    builds = [
        {
            "id": build.id,
            "commit_sha": build.commit_sha,
            "build_date": build.build_date,
            "status": build.status,
            "logs": build.logs,
        }
        for build in all_builds
    ]
    return jsonify(builds)


@app.route("/builds/successes", methods=["GET"])
def get_build_successes():
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
    all_builds = Build.query.filter_by(status="success").all()
    builds = [
        {
            "id": build.id,
            "commit_sha": build.commit_sha,
            "build_date": build.build_date,
            "status": build.status,
            "logs": build.logs,
        }
        for build in all_builds
    ]
    return jsonify(builds)


if __name__ == "__main__":
    app.run(port=5000, debug=False)
