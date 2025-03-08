import os
from pathlib import Path
import unittest

from src.services.email_services import Response
from src.utils.code_quality.syntax import check_syntax
from src.config.test_logger_config import test_logger


class TestSyntaxCheck(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.base_dir = Path(__file__).parent
        self.file_right = os.path.join(self.base_dir, "test_files", "correct.py")
        self.file_wrong = os.path.join(self.base_dir, "test_files", "incorrect.py")
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def setUp(self):
        os.chdir(self.base_dir)
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def test_check_syntax_fail(self):
        """
        Tests if check_syntax fails with a file containing wrong syntax.
        """

        result, _ = check_syntax(self.file_wrong, self.response, test_logger)

        assert not result, "The file doesn't pass the syntax check, when in should pass"

    def test_check_syntax_successful(self):
        """
        Tests if check_syntax succeeds with a file containing the right syntax.
        """

        result, _ = check_syntax(self.file_right, self.response, test_logger)

        assert result, "The file doesn't pass the syntax check, when in should pass"
