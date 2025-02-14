import os
import subprocess


def generate_docs(logging):
    """
    Generate Sphinx documentation for the project's Python modules.

    This function performs the following steps:
    1. Verifies existence of docs/ and code/ directories
    2. Changes working directory to docs/
    3. Runs sphinx-apidoc to generate .rst files from Python modules
    4. Executes make html to build HTML documentation

    Args:
        logging: Logging module instance for recording operations

    Returns:
        None: Function returns early if any step fails

    Raises:
        subprocess.CalledProcessError: If sphinx-apidoc or make html commands fail
        OSError: If directory operations fail
    """
    base_dir = os.path.abspath(os.getcwd())  # Get the absolute base directory
    docs_dir = os.path.join(base_dir, "docs")
    code_dir = os.path.join(base_dir, "code")

    if not os.path.exists(docs_dir):
        logging.error("Error: docs/ directory not found!")
        return
    if not os.path.exists(code_dir):
        logging.error("Error: code/ directory not found!")
        return

    logging.info("Moving to docs directory...")
    os.chdir(docs_dir)

    logging.info("Generating .rst files from Python modules...")
    sphinx_apidoc_cmd = ["sphinx-apidoc", "--force", "-o", "./source", code_dir]
    try:
        process = subprocess.run(
            sphinx_apidoc_cmd, check=True, capture_output=True, text=True
        )
        logging.info(".rst files successfully generated.")
        if process.stdout:
            logging.debug("Sphinx-apidoc output:\n%s", process.stdout)
        if process.stderr:
            logging.warning("Sphinx-apidoc warnings:\n%s", process.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to generate .rst files: {e}")
        if e.stdout:
            logging.debug("Sphinx-apidoc output:\n%s", e.stdout)
        if e.stderr:
            logging.error("Sphinx-apidoc errors:\n%s", e.stderr)
        return

    logging.info("Building HTML documentation...")
    make_html_cmd = ["make", "html"]
    try:
        process = subprocess.run(
            make_html_cmd, check=True, capture_output=True, text=True
        )
        logging.info("Documentation successfully built.")
        if process.stdout:
            logging.debug("Make html output:\n%s", process.stdout)
        if process.stderr:
            logging.warning("Make html warnings:\n%s", process.stderr)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to build HTML documentation: {e}")
        if e.stdout:
            logging.debug("Make html output:\n%s", e.stdout)
        if e.stderr:
            logging.error("Make html errors:\n%s", e.stderr)
        return

#test 5