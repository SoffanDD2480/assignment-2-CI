import os
import unittest

from git_helpers import *

class TestGitHelpers(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.base_dir = os.path.abspath(".")
        self.test_dir = os.path.join(self.base_dir, "test")
        self.repo_name = "test_repo"
        self.branch = "main"
        self.repo_url = "https://github.com/SoffanDD2480/assignment-2-CI.git"

    def setUp(self):
        os.chdir(self.base_dir)

    def test_git_helpers_fail(self):
        """
        Tests if git clone fails with wrong repo
        """

        self.assertRaises(Exception, clone_repo, self.test_dir, self.repo_name, self.branch, "https://github.com/SoffanDD2480/wrong")

    def test_git_helpers_successful(self):
        """
        Tests if git clone works with the right inputs
        """
        res = clone_repo(self.test_dir, self.repo_name, self.branch, self.repo_url)

        assert res == str(os.path.join(self.test_dir, self.repo_name)), "Repo was not cloned to the right location"

        shutil.rmtree(self.test_dir)

    def test_filter_file_fail(self):
        """
        Tests a fail of filtering of commited files, by providing wrong type of data
        """

        self.assertRaises(Exception, filter_files, 1)

    def test_filter_file_successful(self):
        """
        Tests if git clone works with the right inputs
        """

