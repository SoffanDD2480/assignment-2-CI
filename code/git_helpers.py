import os
import shutil
import git


def clone_repo(base_dir: str, repo_name: str, branch: str, repo_url: str) -> str:
    """
    Clone a Git repository to a local directory.

    Args:
        base_dir (str): Base directory where the repository will be cloned
        repo_name (str): Name of the directory that will contain the cloned repository
        branch (str): Branch name to clone
        repo_url (str): URL of the Git repository to clone

    Returns:
        str: Absolute path to the cloned repository directory

    Raises:
        git.GitCommandError: If the clone operation fails
        OSError: If there are file system related errors during directory cleanup
    Example:
        >>> repo_path = clone_repo(
        ...     base_dir="./.sample_dir/",
        ...     repo_name="assignment-2-CI",
        ...     branch="main",
        ...     repo_url="https://github.com/user/repo.git"
        ... )
        >>> print(repo_path)
        './.sample_dir/assignment-2-CI'
    """
    repo_path = os.path.join(base_dir, repo_name)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    git.Repo.clone_from(repo_url, repo_path, branch=branch)
    return repo_path


def filter_files(data):
    """
    Filter changed files from a GitHub webhook push event payload.

    Args:
        data (dict): GitHub webhook push event payload containing commit information

    Returns:
        list: List of Python file paths that were added or modified in the 'code/' directory

    Example:
        >>> data = {
        ...     "commits": [{
        ...         "added": ["code/test.py"],
        ...         "modified": ["code/main.py"]
        ...     }]
        ... }
        >>> filter_files(data)
        ['code/test.py', 'code/main.py']
    """
    # Collect changed files from all commits in the push event.
    changed_files = set()
    for commit in data.get("commits", []):
        for file_path in commit.get("added", []):
            changed_files.add(file_path)
        for file_path in commit.get("modified", []):
            changed_files.add(file_path)
        # We skip removed files.

    # Filter: only include Python files within the 'code/' directory.
    changed_code_files = [
        file_path
        for file_path in changed_files
        if file_path.startswith("code/") and file_path.endswith(".py")
    ]
    print(changed_code_files)
    return changed_code_files

#test 3