import os
from pathlib import Path
import shutil
import unittest

from CI_CD_server.src.utils.path import get_repo_path
from CI_CD_server.src.utils.generate_docs import generate_docs


class TestGenerateDocs(unittest.TestCase):
    project_root: Path
    docs_dir: Path
    build_dir: Path

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.project_root = Path(get_repo_path()).resolve()

    def setUp(self) -> None:
        os.chdir(self.project_root)

    def test_generate_docs_successful(self) -> None:
        """
        Tests if docs are generated in docs/build.

        Deletes the build dir to properly test creation fail.

        Should result in a build directory created, with the docs.
        """
        self.docs_dir = self.project_root / "docs"
        self.build_dir = self.docs_dir / "build"

        if self.build_dir.exists():
            print(f"Removing existing build directory: {self.build_dir}")
            shutil.rmtree(self.build_dir)

        os.makedirs(self.docs_dir, exist_ok=True)
        generate_docs(self.project_root)

        assert (
            self.build_dir.exists()
        ), "There's no build dir in docs/build for the docs"
