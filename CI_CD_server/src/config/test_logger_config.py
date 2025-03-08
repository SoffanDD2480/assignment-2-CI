"""Logging configuration module for test execution.

This module sets up the logging configuration specifically for test runs in the CI/CD pipeline.
It configures a dedicated logger with appropriate formatting for tracking test execution results.
"""

import logging

TEST_LOG_FILE = "test_runs.log"

test_logger = logging.getLogger("test_logger")
logging.basicConfig(
    filename=TEST_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
)
