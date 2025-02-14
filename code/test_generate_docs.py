import os
import shutil
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
        Tests generating files in the wrong directory.

        Deletes the build dir to properly test creation.

        Should result in no build directory created, since it is created in the wrong directory.
        """

        # Establishes base dirs
        code_dir = os.path.abspath("../code")
        build_dir = os.path.abspath("/build")

        # Remove build dir if it exists, to properly test creation fail
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        # Change to the wrong dir, which should result in failed run of generate_docs()
        os.chdir(code_dir)

        generate_docs(logging)

        assert (not os.path.exists(build_dir)), "Build files exist, when they shouldn't"

    def test_generate_docs_successful(self):
        """
        Tests if docs are generated in docs/build.

        Deletes the build dir to properly test creation fail.

        Should result in a build directory created, with the docs.
        """

        # Establishes base dirs
        build_dir = os.path.abspath("/build")

        # Remove build dir if it exists, to properly test creation of the build directory
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        generate_docs(logging)

        assert os.path.exists(build_dir), "There's no build dir in docs/build for the docs"
