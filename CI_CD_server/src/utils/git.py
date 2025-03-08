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
    """

    repo_path = os.path.join(base_dir, repo_name)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    git.Repo.clone_from(repo_url, repo_path, branch=branch)
    return repo_path
