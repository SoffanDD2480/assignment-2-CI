import subprocess


def format_file(file_path, email_response, local_code_file, logging):
    """
    Format a Python file using Black code formatter.

    This function runs `black` on the given file to ensure it is formatted according
    to the Black style guide. If formatting is successful, a success message is logged.
    If an error occurs during formatting, the error message is logged.

    Args:
        file_path (str): The original path of the file in the repository.
        email_response: The email response object to append formatting results.
        local_code_file (str): The local path to the code file to be formatted.
        logging: Logger instance for recording operations

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
