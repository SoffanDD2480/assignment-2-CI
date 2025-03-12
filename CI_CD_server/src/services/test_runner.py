from pathlib import Path
import subprocess

from CI_CD_server.src.services.email_services import Response
from CI_CD_server.src.config.test_logger_config import test_logger, TEST_LOG_FILE


def run_project_tests(
    changed_files: list[str], repo_path: Path, email_response: Response
) -> bool:
    """
    Run tests for all modified Python files in the repository.

    This function:
    1. Runs pytest on the tests directory
    2. Logs detailed results to test_runs.log
    3. Adds pass/fail status to email response
    4. Handles execution errors

    Args:
        changed_files (list[str]): List of Python files that were modified
        repo_path (str): Path to the repository root directory
        email_response (Response): Email response object to append results to

    Returns:
        bool: True if all tests pass, False otherwise

    Raises:
        Exception: Catches and logs any errors during test execution
    """

    # Only run tests if there are changed code files
    if not changed_files:
        msg = "No Python code files were changed. Skipping tests."
        test_logger.info(msg)
        email_response.append_content(msg)
        return True

    tests_dir = repo_path / "CI_CD_server" / "tests"

    # Check if tests directory exists using Path.exists()
    if not tests_dir.exists():
        msg = f"Tests directory not found at: {tests_dir}"
        test_logger.warning(msg)
        email_response.append_content(msg)
        return False

    try:
        # Run pytest on the tests directory
        test_result = subprocess.run(
            ["pytest", tests_dir, "-v"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Log the full test output to the log file
        test_logger.info("Test results:")
        test_logger.info(f"STDOUT:\n{test_result.stdout}")
        test_logger.info(f"STDERR:\n{test_result.stderr}")

        # Add pass/fail status to email
        if test_result.returncode == 0:
            email_response.append_content("✅ All tests passed")
            return True
        else:
            email_response.append_content("❌ Tests failed")
            email_response.append_content(f"Check {TEST_LOG_FILE} for detailed output")
            email_response.passed_tests = False
            return False

    except Exception as e:
        error_msg = f"Error running tests: {str(e)}"
        test_logger.error(error_msg)
        email_response.append_content(error_msg)
        email_response.passed_tests = False
        return False
