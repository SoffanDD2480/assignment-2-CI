from .syntax import check_syntax
from .formatting import format_file


def check_syntax_and_formatting(local_code_file, file_path, email_response, logging):
    """
    Check and format Python source code files.

    This function performs two operations:
    1. Syntax validation using Python's AST parser
    2. Code formatting using Black (if syntax check passes)

    Args:
        local_code_file (str): Path to the local copy of the file to check
        file_path (str): Original repository path of the file (for logging/reporting)
        email_response: Email response object to append results
        logging: Logger instance for recording operations

    Returns:
        bool: True if syntax is valid and formatting succeeded, False otherwise
        Message: Error message if syntax check fails
    """

    syntax_checked, error_message = check_syntax(
        local_code_file, email_response, logging
    )

    if not syntax_checked:
        email_response.append_content(f"Syntax error found in {file_path}.")
        logging.warn(f"Syntax check failed for {file_path}. Aborting.")
        return False, error_message

    email_response.append_content(f"Syntax check passed for {file_path}.")
    logging.info(f"Syntax check passed for {file_path}.")

    formatting_checked = format_file(
        file_path, email_response, local_code_file, logging
    )

    if not formatting_checked:
        return False, "Formatting failed."

    success_message = f"Syntax check and formatting passed for {file_path}."
    email_response.append_content(success_message)
    logging.info(success_message)

    return True, ""
