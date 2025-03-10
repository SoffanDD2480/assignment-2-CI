import os
import shutil
import unittest
from pathlib import Path

from src.utils.path import get_repo_path
from src.utils.filter import filter_files
from src.utils.git import clone_repo


class TestGitHelpers(unittest.TestCase):
    base_dir: Path
    test_dir: Path
    repo_name: str
    branch: str
    repo_url: str

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.base_dir = Path(get_repo_path()).resolve()
        self.test_dir = self.base_dir / "test"
        self.repo_name = "test_repo"
        self.branch = "main"
        self.repo_url = "https://github.com/SoffanDD2480/assignment-2-CI.git"

    def setUp(self) -> None:
        os.chdir(self.base_dir)

    def test_git_helpers_fail(self) -> None:
        """
        Tests if git clone fails with wrong repo
        """
        self.assertRaises(
            Exception,
            clone_repo,
            self.test_dir,
            self.repo_name,
            self.branch,
            "https://github.com/SoffanDD2480/wrong",
        )

    def test_git_helpers_successful(self) -> None:
        """
        Tests if git clone works with the right inputs
        """
        res = clone_repo(self.test_dir, self.repo_name, self.branch, self.repo_url)

        expected_path = self.test_dir / self.repo_name
        assert res == expected_path, "Repo was not cloned to the right location"

        # Clean up after test
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_filter_file_fail(self) -> None:
        """
        Tests a fail of filtering of commited files, by providing wrong type of data
        """
        self.assertRaises(Exception, filter_files, 1)

    def test_filter_file_successful(self) -> None:
        """
        Tests if git clone works with the right inputs
        """
        # Simulates commit data
        data = {
            "commits": [
                {
                    "added": ["code/test_git_helpers.py"],
                    "modified": ["code/build_db.py", "README.md"],
                }
            ]
        }

        res = filter_files(data)

        assert set(res) == {
            "code/test_git_helpers.py",
            "code/build_db.py",
        }, "Filter function didn't filter the right files"
