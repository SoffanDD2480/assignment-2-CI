import os
import shutil
import subprocess
import logging
import unittest

from generate_docs import generate_docs

class TestGenerateDocs(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.base_dir = os.path.abspath(".")

    def setUp(self):
        os.chdir(self.base_dir)

    def test_generate_docs_fail(self):
        """
        Tests generating files in the wrong directory

        :return: None
        """
        code_dir = os.path.abspath("code")
        build_dir = os.path.abspath("docs/build")

        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        os.chdir(code_dir)

        generate_docs(logging)

        assert (not os.path.exists(build_dir)), "Build files exist, when they shouldn't"

    def test_generate_docs_successful(self):
        """
        Tests if docs are generated in docs/build

        :return: None
        """
        build_dir = os.path.abspath("docs/build")

        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        generate_docs(logging)

        assert os.path.exists(build_dir), "There's no build dir in docs/build for the docs"
