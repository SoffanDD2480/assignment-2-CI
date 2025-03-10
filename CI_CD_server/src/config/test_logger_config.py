"""Logging configuration module for the CI/CD servers test runs.

This module sets up the logging configuration for the CI/CD servers test runs application.
It configures the logger with appropriate formatting and output destinations.
"""

import logging
from pathlib import Path

# This assumes the config file is at CI_CD_server/src/config/
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parents[2]

logs_dir = project_root / "logs"
logs_dir.mkdir(exist_ok=True)

TEST_LOG_FILE = logs_dir / "test_runs.log"

test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.INFO)

if not test_logger.handlers:
    file_handler = logging.FileHandler(str(TEST_LOG_FILE))
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(formatter)

    test_logger.addHandler(file_handler)
