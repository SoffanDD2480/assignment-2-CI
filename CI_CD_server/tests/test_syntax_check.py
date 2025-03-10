import os
from pathlib import Path
import unittest

from src.services.email_services import Response
from src.utils.code_quality.syntax import check_syntax


class TestSyntaxCheck(unittest.TestCase):
    base_dir: Path
    file_right: Path
    file_wrong: Path
    response: Response

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.base_dir = Path(__file__).parent.resolve()
        self.file_right = self.base_dir / "test_files" / "correct.py"
        self.file_wrong = self.base_dir / "test_files" / "incorrect.py"
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def setUp(self) -> None:
        os.chdir(self.base_dir)
        self.response = Response(("Test Testsson", "tt@test.test"), "test")

    def test_check_syntax_fail(self) -> None:
        """
        Tests if check_syntax fails with a file containing wrong syntax.
        """

        result: bool
        result, _ = check_syntax(self.file_wrong, self.response)

        assert not result, "The file doesn't pass the syntax check, when in should pass"

    def test_check_syntax_successful(self) -> None:
        """
        Tests if check_syntax succeeds with a file containing the right syntax.
        """

        result: bool
        result, _ = check_syntax(self.file_right, self.response)

        assert result, "The file doesn't pass the syntax check, when in should pass"
