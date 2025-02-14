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
    Check and format Python source code files.

    This function performs two operations:
    1. Syntax validation using Python's AST parser
    2. Code formatting using Black (if syntax check passes)

    Args:
        local_code_file (str): Path to the local copy of the file to check
        file_path (str): Original repository path of the file (for logging/reporting)
        email_response (Response): Email response object to append results
        logging: Logger instance for recording operations

    Returns:
        bool: True if syntax is valid and formatting succeeded, False otherwise

    Example:
        >>> from email_response import Response
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> email_response = Response(("John", "john@example.com"), "main")
        >>> result = check_syntax_and_formatting(
        ...     "local/path/main.py",
        ...     "code/main.py",
        ...     email_response,
        ...     logging
        ... )
        >>> print(result)
        True
    """

    syntax_checked, error_message = check_syntax(local_code_file, email_response, logging)

    if not syntax_checked:
        email_response.append_content(f"Syntax error found in {file_path}.")
        logging.warn(f"Syntax check passed for {file_path}. Aborting.")
        return False, error_message
    
    email_response.append_content(f"Syntax check passed for {file_path}.")
    logging.info(f"Syntax check passed for {file_path}.")

    formatting_checked = format_file(file_path, email_response, local_code_file, logging)

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

    Args:
        file_path (str): Path to the Python file to check
        email_response (Response): Object to store email content.
        logging: Logger instance for recording operations

    Returns:
        bool: True if syntax is valid, False if parsing errors found

    Example:
        >>> import logging
        >>> logging.basicConfig(level=logging.INFO)
        >>> is_valid = check_syntax("path/to/valid.py", logging)
        >>> print(is_valid)
        True
        >>> is_valid = check_syntax("path/to/invalid.py", logging)
        >>> print(is_valid)
        False

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

     Example:
        >>> # Setup logging and email response
        >>> import logging
        >>> from email_response import Response
        >>> logging.basicConfig(level=logging.INFO)
        >>> email_response = Response(("John", "john@example.com"), "main")
        >>>
        >>> # Example with valid Python file
        >>> result = check_syntax_and_formatting(
        ...     "local/path/valid.py",
        ...     "code/valid.py",
        ...     email_response,
        ...     logging
        ... )
        >>> print(result)
        True
        >>>
        >>> # Example with syntax error
        >>> result = check_syntax_and_formatting(
        ...     "local/path/invalid.py",
        ...     "code/invalid.py",
        ...     email_response,
        ...     logging
        ... )
        >>> print(result)
        False
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
# Test 3