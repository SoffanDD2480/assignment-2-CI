import subprocess
from email_response import Response
import ast


def check_syntax_and_formatting(local_code_file, file_path, email_response, logging):
    """
    Check the syntax of a file. If the syntax is incorrect,
    run the formatter and check again.

    Returns True if the syntax check passes (either before or
    after formatting), otherwise returns False.
    """
    if check_syntax(local_code_file, logging):
        email_response.append_content(f"Syntax check passed for {file_path}.")
        logging.info(f"Syntax check passed for {file_path}.")

        email_response.append_content(f"Running formatter on {file_path}.")
        logging.info(f"Running formatter on {file_path}.")
        format_file(file_path, email_response, local_code_file, logging)
        return True
    else:
        email_response.append_content(f"Syntax error found in {file_path}. Aborting.")
        logging.warn(f"Syntax error found in {file_path}. Aborting.")
        return False


# Check the syntax of a Python file.
def check_syntax(file_path, logging):
    """
    Check the syntax of a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        bool: True if the file's syntax is valid, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        # parse code.
        ast.parse(source, filename=file_path)
        return True
    except Exception:
        return False


# Format the file using Black.
def format_file(file_path, email_response: Response, local_code_file, logging):
    """
    Format a Python file using Black code formatter.

    Args:
        file_path (str): The original path of the file in the repository.
        email_response (Response): The email response object to append formatting results.
        local_code_file (str): The local path to the code file to be formatted.

    Returns:
        subprocess.CompletedProcess: The result of the Black formatting if successful.
        None: If the formatting fails.
    """
    try:
        result = subprocess.run(
            ["black", local_code_file],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        email_response.append_content(f"Formatted {file_path} with Black.")
        logging.info(f"Formatted {file_path} with Black.")
        return result
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        email_response.append_content(
            f"Error formatting {file_path} with Black: {error_message}"
        )
        logging.warn(f"Error formatting {file_path} with Black: {error_message}")
        # Skip to the next file if formatting fails.
        return None
