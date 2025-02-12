import subprocess
from email_response import Response
import ast


def check_syntax_and_formatting(local_code_file, file_path, email_response, logging):
    """
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
    Validate Python file syntax using AST parser.

    Args:
        file_path (str): Path to the Python file to check
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
