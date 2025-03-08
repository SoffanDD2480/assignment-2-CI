import os
import re
from flask import current_app

from src.utils.git import clone_repo
from src.utils.filter import filter_files
from src.utils.code_quality.quality_check import check_syntax_and_formatting
from src.services.test_runner import test_changed_code_files
from src.utils.generate_docs import generate_docs
from src.services.email_services import Response


def process_webhook_event(data, logging):
    """
    Process a webhook event from GitHub.

    Args:
        data (dict): The webhook event payload
        logging: Logger instance for recording operations

    Returns:
        tuple: (result_info, overall_success)
    """
    overall_success = True

    # Extract data from the webhook payload
    current_branch = data.get("ref", "")
    current_branch = re.search(r"refs/heads/(.+)", current_branch).group(1)
    pusher_info = data.get("pusher", {})
    pusher_name = pusher_info.get("name")
    pusher_email = pusher_info.get("email")

    # Create notification object
    email_response = Response((pusher_name, pusher_email), current_branch)

    logging.info(
        f"Processing push event from {pusher_name} ({pusher_email}) on branch {current_branch}."
    )

    # Configuration settings
    base_dir = current_app.config.get("BASE_DIR")
    repo_name = current_app.config.get("REPO_NAME")
    repo_url = current_app.config.get("REPO_URL")

    # Clone the repository
    repo_path = clone_repo(base_dir, repo_name, current_branch, repo_url)
    logging.info(f"Repository cloned to {repo_path}.")

    # Generate documentation
    generate_docs(logging)
    logging.info("Docs generated.")

    # Filter changed files
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
            passed_syntax, error_message = check_syntax_and_formatting(
                local_code_file, file_path, email_response, logging
            )

            if not passed_syntax:
                # If syntax fails, skip tests for this file
                email_response.set_syntax_result(False)
                email_response.append_content(error_message)
                overall_success = False
                continue

        # Run tests for all changed files
        test_results = test_changed_code_files(
            changed_code_files, repo_path, email_response
        )

        if not test_results:
            email_response.set_tests_result(False)
            overall_success = False

    logging.info(f"Webhook processed for branch: {current_branch}" + "\n")

    email_response.make_response()
    if not current_app.debug:
        email_response.send_response()
        logging.info(f"Sent email contents: {email_response.body}")
    else:
        print("Debug mode: Email would have been sent with content:")
        print(email_response.body)
        print("END OF EMAIL CONTENT\n")
        logging.info(
            f"Debug mode: Email content that would have been sent: {email_response.body}."
        )

    return email_response, overall_success
