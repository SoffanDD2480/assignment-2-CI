def filter_files(data):
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

    return changed_files
