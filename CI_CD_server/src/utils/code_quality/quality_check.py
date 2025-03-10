from pathlib import Path

from .syntax import check_syntax
from .formatting import format_file
from src.services.email_services import Response
from src.config.server_logger_config import server_logger


def check_syntax_and_formatting(
    local_code_file: Path, file_path: str, email_response: Response
) -> tuple[bool, str]:
    """
    Check and format Python source code files.

    This function performs two operations:
    1. Syntax validation using Python's AST parser
    2. Code formatting using Black (if syntax check passes)

    Args:
        local_code_file (path): Path to the local copy of the file to check
        file_path (str): Original repository path of the file (for server_logger/reporting)
        email_response: Email response object to append results

    Returns:
        bool: True if syntax is valid and formatting succeeded, False otherwise
        Message: Error message if syntax check fails
    """

    syntax_checked, error_message = check_syntax(local_code_file, email_response)

    if not syntax_checked:
        email_response.append_content(f"Syntax error found in {file_path}.")
        server_logger.warning(f"Syntax check failed for {file_path}. Aborting.")
        return False, error_message

    email_response.append_content(f"Syntax check passed for {file_path}.")
    server_logger.info(f"Syntax check passed for {file_path}.")

    formatting_checked = format_file(file_path, local_code_file, email_response)

    if not formatting_checked:
        return False, "Formatting failed."

    success_message = f"Syntax check and formatting passed for {file_path}."
    email_response.append_content(success_message)
    server_logger.info(success_message)

    return True, ""
