from flask import Blueprint, request, jsonify

from src.services.ci_service import process_webhook_event
from src.models.build import Build
from src.config.server_logger_config import server_logger

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def webhook() -> tuple[dict, int]:
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
    """
    server_logger.info("Received webhook request.")

    # Process only push events.
    if request.headers.get("X-Github-Event") != "push":
        server_logger.info("Ignored event (not a push event).")
        return jsonify({"message": "Not a push event"}), 200

    try:
        data = request.get_json()
        commit_sha = data.get("after", "unknown")

        # Process the webhook through the service
        overall_success = process_webhook_event(data)
        build_status = "success" if overall_success else "failure"

        Build.add_build(commit_sha, build_status)

        server_logger.info("Webhook processed.")
        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        server_logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
