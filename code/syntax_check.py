import subprocess
import logging
from email_response import Response


def check_syntax_and_formatting(local_code_file, file_path, email_response, logging):
    """
    This function first checks the syntax of the given Python file using `pylint`. 
    If the syntax check fails, it logs an error and stops further processing.
    If the syntax check passes, it proceeds to format the file using `black`.

    Returns a tuple: (bool, str)
    - True, "" if syntax check and formatting pass.
    - False, error_message if syntax check fails.
    """

    syntax_checked, error_message = check_syntax(local_code_file, email_response, logging)

    if not syntax_checked:
        email_response.append_content(f"Syntax error found in {file_path}.")
        logging.warn(f"Syntax check passed for {file_path}. Aborting.")
        return False, error_message
    
    email_response.append_content(f"Syntax check passed for {file_path}.")
    logging.info(f"Syntax check passed for {file_path}.")

    formatting_checked = format_file(local_code_file, file_path, email_response, logging)

    if not formatting_checked:
        return False, "Formatting failed."
    
    success_message = f"Syntax check and formatting passed for {file_path}."
    email_response.append_content(success_message)
    logging.info(success_message)

    return True, ""


# Check the syntax of a Python file.
def check_syntax(file_path, email_response, logging):
    """
    Check the syntax of a Python file using pylint.

    This function runs `pylint --errors-only` to detect syntax errors in the given file.
    If syntax errors are found, they are logged and stored in the email response.
    If the file passes the syntax check, a success message is logged

    Args:
        file_path (str): The path to the Python file.
        email_response (Response): Object to store email content.
        logging: Logging module.
        
    Returns:
        tuple: (bool, str) -> True if syntax check passes, False otherwise.
    """

    try:
        result = subprocess.run(
            ["pylint", "--errors-only", file_path],capture_output=True,text=True
        )

        pylint_output = result.stdout.strip()


        if result.returncode != 0:
            error_message = f"Syntax errors detected in {file_path}:\n{pylint_output}"
            logging.error(error_message)
            email_response.append_content(error_message)
            return False, pylint_output  

        success_message = f"Syntax check passed for {file_path}."
        logging.info(success_message)
        email_response.append_content(success_message)
        return True, ""

    except FileNotFoundError:
        error_message = f"Error: pylint not found for {file_path}."
        logging.error(error_message)
        email_response.append_content(error_message)
        return False, error_message
    
    except Exception as e:
        logging.error(f"Unexpected error during syntax check: {e}")
        return False, str(e)


# Format the file using Black.
def format_file(file_path, email_response: Response, local_code_file, logging):
    """
    Format a Python file using Black code formatter.
    
    This function runs `black` on the given file to ensure it is formatted according 
    to the Black style guide. If formatting is successful, a success message is logged. 
    If an error occurs during formatting, the error message is logged.

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
