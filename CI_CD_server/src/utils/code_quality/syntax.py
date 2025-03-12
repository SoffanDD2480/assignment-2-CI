from pathlib import Path
import subprocess
from CI_CD_server.src.services.email_services import Response
from CI_CD_server.src.config.server_logger_config import server_logger


def check_syntax(file_path: Path, email_response: Response) -> tuple[bool, str]:
    """
    Check the syntax of a Python file using pylint.

    This function runs `pylint --errors-only` to detect syntax errors in the given file.
    If syntax errors are found, they are logged and stored in the email response.
    If the file passes the syntax check, a success message is logged

    Args:
        file_path (str): Path to the Python file to check
        email_response: Object to store email content.

    Returns:
        tuple: (bool, str) -> True if syntax is valid, False if parsing errors found
    """

    try:
        result = subprocess.run(
            ["pylint", "--errors-only", file_path], capture_output=True, text=True
        )
        pylint_output = result.stdout.strip()

        if result.returncode != 0:
            server_logger.error(
                f"Syntax errors detected in {file_path}:\n{pylint_output}"
            )
            return False, pylint_output

        server_logger.info(f"Syntax check passed for {file_path}.")
        return True, ""

    except FileNotFoundError:
        error_message = f"Error: pylint not found for {file_path}."
        server_logger.error(error_message)
        email_response.append_content(error_message)
        return False, error_message

    except Exception as e:
        server_logger.error(f"Unexpected error during syntax check: {e}")
        return False, str(e)
