import os
import shutil
import subprocess
import logging

from generate_docs import generate_docs


def test_generate_docs_successful():
    """
    Tests if docs are generated in docs/build

    :return: None
    """

    build_dir = os.path.abspath("docs/build")

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    generate_docs(logging)

    assert os.path.exists(build_dir), "There's no build dir in docs/build for the docs"
