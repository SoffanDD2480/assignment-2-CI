import os
import unittest

from syntax_check import *
from email_response import Response

class TestSyntaxCheck(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.base_dir = os.path.abspath(".")
        self.test_file_right = os.path.join(self.base_dir, "code", "test_file_right.py")
        self.test_file_wrong = os.path.join(self.base_dir, "code", "test_file_wrong.py")
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def setUp(self):
        os.chdir(self.base_dir)
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def test_check_syntax_fail(self):
        """
        Tests if check_syntax fails with a file containing wrong syntax.
        """

        result, _ = check_syntax(self.test_file_wrong, self.response, logging)

        assert not result, "The file doesn't pass the syntax check, when in should pass"


    def test_check_syntax_successful(self):
        """
        Tests if check_syntax succeeds with a file containing the right syntax.
        """

        result, _ = check_syntax(self.test_file_right, self.response, logging)

        assert result, "The file doesn't pass the syntax check, when in should pass"

