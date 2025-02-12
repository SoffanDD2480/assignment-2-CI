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
    for file_path in changed_code_files:
        base_filename = os.path.basename(file_path)
        test_filename = f"test_{base_filename}"
        local_test_file = os.path.join(repo_path, "tests", test_filename)

        if os.path.exists(local_test_file):
            try:
                # Run pytest with minimal output
                test_result = subprocess.run(
                    ["pytest", local_test_file, "-q", "--no-header"],
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                # Log the full test output to the log file
                test_logger.info(f"Test results for {file_path}:")
                test_logger.info(f"STDOUT:\n{test_result.stdout}")
                test_logger.info(f"STDERR:\n{test_result.stderr}")

                # Only add pass/fail status to email
                if test_result.returncode == 0:
                    email_response.append_content(f"✅ Tests passed for {file_path}")
                else:
                    email_response.append_content(f"❌ Tests failed for {file_path}")
                    email_response.append_content(
                        f"Check {TEST_LOG_FILE} for detailed output"
                    )

            except Exception as e:
                error_msg = f"Error running tests for {file_path}: {str(e)}"
                test_logger.error(error_msg)
                email_response.append_content(error_msg)
        else:
            msg = f"No test file found for {file_path} at expected location: tests/{test_filename}"
            test_logger.warning(msg)
            email_response.append_content(msg)
