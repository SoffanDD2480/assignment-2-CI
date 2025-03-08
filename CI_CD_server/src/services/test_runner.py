import os
import subprocess

from src.config.test_logger_config import test_logger, TEST_LOG_FILE


def test_changed_code_files(changed_code_files, repo_path, email_response):
    """
    Run tests for all modified Python files in the repository.

    This function:
    1. Runs pytest on the tests directory
    2. Logs detailed results to test_runs.log
    3. Adds pass/fail status to email response
    4. Handles execution errors

    Args:
        changed_code_files (list[str]): List of Python files that were modified
        repo_path (str): Path to the repository root directory
        email_response (Response): Email response object to append results to

    Returns:
        bool: True if all tests pass, False otherwise

    Raises:
        Exception: Catches and logs any errors during test execution

    Example:
        >>> from email_response import Response
        >>> email_response = Response(("John", "john@example.com"), "main")
        >>> changed_files = ["code/calculator.py", "code/utils.py"]
        >>> repo_path = "/path/to/repository"
        >>> test_changed_code_files(changed_files, repo_path, email_response)
        # Output in test_runs.log:
        # 2025-02-12 10:30:15 - INFO - Test results:
        # 2025-02-12 10:30:15 - INFO - STDOUT: 5 passed in 0.27s
    """

    # Only run tests if there are changed code files
    if not changed_code_files:
        msg = "No Python code files were changed. Skipping tests."
        test_logger.info(msg)
        email_response.append_content(msg)
        return True

    tests_dir = os.path.join(repo_path, "tests")

    # Check if tests directory exists
    if not os.path.exists(tests_dir):
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
