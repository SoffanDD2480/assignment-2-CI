"""Utility functions for handling file paths in the project.

This module provides helper functions for resolving paths relative to the
project root and ensuring consistent path handling across the codebase.
"""

from pathlib import Path


def get_absolute_path(relative_path: Path) -> Path:
    """Convert a relative path to an absolute path based on project root.

    Args:
        relative_path (str): A path relative to the project root

    Returns:
        Path: The absolute path as a Path object

    Examples:
        >>> get_absolute_path("docs/source")
        PosixPath('/Users/username/Programming/Github/assignment-2-CI/docs/source')
    """
    # Get the directory of the current file (path.py)
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent

    # Navigate up to the project root (3 levels up from utils module)
    # utils -> src -> CI_CD_server -> project_root
    project_root = current_dir.parents[2]

    # Join with the relative path and return
    return project_root / relative_path


def get_repo_path() -> Path:
    """Get the absolute path to the repository root.

    Returns:
        Path: The absolute path to the repository root as a Path object
    """
    return get_absolute_path(Path(""))
