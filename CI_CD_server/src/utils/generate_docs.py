import os
import subprocess
from pathlib import Path
from src.config.server_logger_config import server_logger


def generate_docs(repo_path: Path) -> None:
    """
    Generate Sphinx documentation for the project's Python modules.

    This function performs the following steps:
    1. Verifies existence of docs/ and CI_CD_server/ directories
    2. Changes working directory to docs/
    3. Runs sphinx-apidoc to generate .rst files from Python modules
    4. Executes make html to build HTML documentation

    Args:
        repo_path: Path to the root directory of the repository

    Returns:
        None: Function returns early if any step fails

    Raises:
        subprocess.CalledProcessError: If sphinx-apidoc or make html commands fail
        OSError: If directory operations fail
    """

    docs_dir = repo_path / "docs"

    if not docs_dir.exists():
        server_logger.error(f"Error: docs/ {docs_dir} directory not found!")
        return

    server_logger.info(f"Moving to {docs_dir} directory...")
    os.chdir(docs_dir)

    server_logger.info("Generating .rst files from Python modules...")
    sphinx_apidoc_cmd = ["sphinx-apidoc", "-f", "-M", "-o", "./source", "./../"]
    try:
        process = subprocess.run(
            sphinx_apidoc_cmd, check=True, capture_output=True, text=True
        )
        server_logger.info(".rst files successfully generated.")
        if process.stdout:
            server_logger.debug("Sphinx-apidoc output:\n%s", process.stdout)
        if process.stderr:
            server_logger.warning("Sphinx-apidoc warnings:\n%s", process.stderr)
    except subprocess.CalledProcessError as e:
        server_logger.error(f"Failed to generate .rst files: {e}")
        if e.stdout:
            server_logger.debug("Sphinx-apidoc output:\n%s", e.stdout)
        if e.stderr:
            server_logger.error("Sphinx-apidoc errors:\n%s", e.stderr)
        return

    server_logger.info("Building HTML documentation...")
    make_html_cmd = ["make", "html"]
    try:
        process = subprocess.run(
            make_html_cmd, check=True, capture_output=True, text=True
        )
        server_logger.info("Documentation successfully built.")
        if process.stdout:
            server_logger.debug("Make html output:\n%s", process.stdout)
        if process.stderr:
            server_logger.warning("Make html warnings:\n%s", process.stderr)
    except subprocess.CalledProcessError as e:
        server_logger.error(f"Failed to build HTML documentation: {e}")
        if e.stdout:
            server_logger.debug("Make html output:\n%s", e.stdout)
        if e.stderr:
            server_logger.error("Make html errors:\n%s", e.stderr)
        return
