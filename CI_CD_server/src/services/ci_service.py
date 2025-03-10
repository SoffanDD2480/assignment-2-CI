import re
from pathlib import Path
from flask import current_app

from src.utils.git import clone_repo
from src.utils.filter import filter_files
from src.utils.code_quality.quality_check import check_syntax_and_formatting
from src.services.test_runner import run_project_tests
from src.utils.generate_docs import generate_docs
from src.services.email_services import Response
from src.config.server_logger_config import server_logger


def process_webhook_event(data: dict) -> bool:
    """
    Process a webhook event from GitHub.

    Args:
        data (dict): The webhook event payload

    Returns:
        tuple: (result_info, overall_success)
    """
    overall_success = True

    # Extract data from the webhook payload
    current_branch = data.get("ref", "")
    branch_match = re.search(r"refs/heads/(.+)", current_branch)
    if branch_match:
        current_branch = branch_match.group(1)
    else:
        current_branch = "main"  # Default if pattern doesn't match
    pusher_info = data.get("pusher", {})
    pusher_name = pusher_info.get("name")
    pusher_email = pusher_info.get("email")

    # Create notification object
    email_response = Response((pusher_name, pusher_email), current_branch)

    server_logger.info(
        f"Processing push event from {pusher_name} ({pusher_email}) on branch {current_branch}."
    )

    # Configuration settings
    base_dir = Path(current_app.config.get("BASE_DIR")).resolve()
    repo_name = current_app.config.get("REPO_NAME")
    repo_url = current_app.config.get("REPO_URL")

    # Clone the repository
    repo_path = Path(
        clone_repo(base_dir, repo_name, current_branch, repo_url)
    ).resolve()
    server_logger.info(f"Repository cloned to {repo_path}.")

    # Generate documentation
    generate_docs(repo_path)
    server_logger.info("Docs generated.")

    # Filter changed files
    changed_files = filter_files(data)

    if not changed_files:
        server_logger.info("No Python code changes detected.")
        email_response.append_content("No Python code changes detected.")
    else:
        for file_path in changed_files:
            local_code_file = repo_path / file_path
            email_response.append_content(f"Processing changed file: {file_path}")
            server_logger.info(f"Processing changed file: {file_path}")

            # Check syntax and auto-format
            passed_syntax, error_message = check_syntax_and_formatting(
                local_code_file, file_path, email_response
            )

            if not passed_syntax:
                # If syntax fails, skip tests for this file
                email_response.set_syntax_result(False)
                email_response.append_content(error_message)
                overall_success = False
                continue

        # Run tests for all changed files
        test_results = run_project_tests(changed_files, repo_path, email_response)

        if not test_results:
            email_response.set_tests_result(False)
            overall_success = False

    server_logger.info(f"Webhook processed for branch: {current_branch}" + "\n")

    email_response.make_response()
    if not current_app.debug:
        email_response.send_response()
        server_logger.info(f"Sent email contents: {email_response.body}")
    else:
        print("Debug mode: Email would have been sent with content:")
        print(email_response.body)
        print("END OF EMAIL CONTENT\n")
        server_logger.info(
            f"Debug mode: Email content that would have been sent: {email_response.body}."
        )

    return overall_success
