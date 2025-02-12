import os
import logging

from flask import Flask, request, jsonify
from syntax_check import check_syntax_and_formatting
from email_response import Response
from git_helpers import clone_repo, filterFiles
from tests import test_changed_code_files

app = Flask(__name__)

# Base directory and repository details.
BASE_DIR = "./.sample_dir/"
REPO_NAME = "assignment-2-CI"
REPO_URL = "https://github.com/SoffanDD2480/assignment-2-CI.git"
LOG_FILE = "server.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@app.route("/webhook", methods=["POST"])
def webhook():
    logging.info("Received webhook request.")
    # Process only push events.
    if request.headers.get("X-Github-Event") != "push":
        logging.info("Ignored event (not a push event).")
        return jsonify({"message": "Not a push event"}), 200

    try:
        data = request.get_json()
        current_branch = data.get("ref", "").split("/")[-1]
        pusher_info = data.get("pusher", {})
        pusher_name = pusher_info.get("name")
        pusher_email = pusher_info.get("email")
        email_response = Response((pusher_name, pusher_email), current_branch)

        logging.info(
            f"Processing push event from {pusher_name} ({pusher_email}) on branch {current_branch}."
        )

        # Clone the repository into BASE_DIR/REPO_NAME.
        repo_path = clone_repo(BASE_DIR, REPO_NAME, current_branch, REPO_URL)
        logging.info(f"Repository cloned to {repo_path}.")

        changed_code_files = filterFiles(data)

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

        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=False)
