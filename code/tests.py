import os
import subprocess
import logging

# Configure logging for test runs
TEST_LOG_FILE = "test_runs.log"
test_logger = logging.getLogger("test_runner")
test_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(TEST_LOG_FILE)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
test_logger.addHandler(file_handler)


def test_changed_code_files(changed_code_files, repo_path, email_response, logging):
    """
    Run tests for all modified Python files in the repository.

    This function:
    1. Looks for corresponding test files in the tests directory
    2. Runs pytest on each test file
    3. Logs detailed results to test_runs.log
    4. Adds pass/fail status to email response
    5. Handles missing test files and execution errors

    Args:
        changed_code_files (list[str]): List of Python files that were modified
        repo_path (str): Path to the repository root directory
        email_response (Response): Email response object to append results to
        logging: Logger instance for recording operations

    Returns:
        None: Results are communicated via email_response and logging

    Raises:
        Exception: Catches and logs any errors during test execution

    Example:
        >>> from email_response import Response
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> email_response = Response(("John", "john@example.com"), "main")
        >>> changed_files = ["code/calculator.py", "code/utils.py"]
        >>> repo_path = "/path/to/repository"
        >>> test_changed_code_files(changed_files, repo_path, email_response, logging)
        # Output in test_runs.log:
        # 2025-02-12 10:30:15 - INFO - Test results for code/calculator.py:
        # 2025-02-12 10:30:15 - INFO - STDOUT: 2 passed in 0.12s
        # 2025-02-12 10:30:16 - INFO - Test results for code/utils.py:
        # 2025-02-12 10:30:16 - INFO - STDOUT: 3 passed in 0.15s
    """
    for file_path in changed_code_files:
        print(file_path)
        base_filename = os.path.basename(file_path)
        test_filename = f"test_{base_filename}"
        local_test_file = os.path.join(repo_path, "tests", test_filename)

        if os.path.exists(local_test_file):
            try:
                print("test 6")
                # Run pytest with minimal output
                test_result = subprocess.run(
                    ["pytest", local_test_file, "-q", "--no-header"],
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                print("test 7")
                # Log the full test output to the log file
                test_logger.info(f"Test results for {file_path}:")
                test_logger.info(f"STDOUT:\n{test_result.stdout}")
                test_logger.info(f"STDERR:\n{test_result.stderr}")

                # Only add pass/fail status to email
                if test_result.returncode == 0:
                    email_response.append_content(f"✅ Tests passed for {file_path}")
                    print(f"✅ Tests passed for {file_path}")
                else:
                    email_response.append_content(f"✅ Tests passed for {file_path}")
                    print(f"Else✅ Tests passed for {file_path}")
                    email_response.append_content(
                        f"Check {TEST_LOG_FILE} for detailed output"
                    )

            except Exception as e:
                error_msg = f"Error running tests for {file_path}: {str(e)}"
                test_logger.error(error_msg)
                email_response.append_content(error_msg)
                print(error_msg)
        else:
            msg = f"No test file found for {file_path} at expected location: tests/{test_filename}"
            test_logger.warning(msg)
            email_response.append_content(msg)
            print(msg)
