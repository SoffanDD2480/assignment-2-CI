"""Logging configuration module for the CI/CD server.

This module sets up the logging configuration for the CI/CD server application.
It configures the logger with appropriate formatting and output destinations.
"""

import logging

LOG_FILE = "server.log"

test_logger = logging.getLogger("server_logger")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)
