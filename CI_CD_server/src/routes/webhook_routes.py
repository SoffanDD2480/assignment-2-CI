import logging
import io
from flask import Blueprint, request, jsonify

from src.services.ci_service import process_webhook_event
from src.models.build import Build

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    """
    Handle GitHub webhook POST requests for push events.

    [original docstring content]
    """
    log_capture_string = io.StringIO()
    mem_handler = logging.StreamHandler(log_capture_string)
    mem_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    mem_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(mem_handler)

    logging.info("Received webhook request.")

    # Process only push events.
    if request.headers.get("X-Github-Event") != "push":
        logging.info("Ignored event (not a push event).")
        return jsonify({"message": "Not a push event"}), 200

    try:
        data = request.get_json()
        commit_sha = data.get("after", "unknown")

        # Process the webhook through the service
        overall_success = process_webhook_event(data, logging)

        # Record the build
        mem_handler.flush()
        build_logs = log_capture_string.getvalue()
        build_status = "success" if overall_success else "failure"

        Build.add_build(commit_sha, build_logs, build_status)

        logging.info("Webhook processed.")
        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
