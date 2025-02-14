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

    def test_generate_docs_successful(self):
        """
        Tests if docs are generated in docs/build.

        Deletes the build dir to properly test creation fail.

        Should result in a build directory created, with the docs.
        """

        self.base_dir = os.path.abspath(".")
        self.docs_dir = os.path.join(self.base_dir, "docs")
        self.build_dir = os.path.join(self.docs_dir, "build")

        if os.path.exists(self.build_dir):
            print(f"Removing existing build directory: {self.build_dir}")
            shutil.rmtree(self.build_dir)


        os.makedirs(self.docs_dir, exist_ok=True)
        generate_docs(logging)

        assert os.path.exists(self.build_dir), "There's no build dir in docs/build for the docs"

