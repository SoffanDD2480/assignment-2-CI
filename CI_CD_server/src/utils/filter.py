def filter_files(data: dict) -> list[str]:
    """
    Filter changed files from a GitHub webhook push event payload.

    Args:
        data (dict): GitHub webhook push event payload containing commit information

    Returns:
        list: List of Python file paths that were added or modified
    """

    # Collect changed files from all commits in the push event.
    changed_files = set()
    for commit in data.get("commits", []):
        for file_path in commit.get("added", []):
            changed_files.add(file_path)
        for file_path in commit.get("modified", []):
            changed_files.add(file_path)
        # We skip removed files.

    # Filter out non-Python files
    changed_python_files = [file for file in changed_files if file.endswith(".py")]

    return changed_python_files
