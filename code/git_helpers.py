import os
import shutil
import git


def clone_repo(base_dir: str, repo_name: str, branch: str, repo_url: str) -> str:
    """
    Clones the repository at repo_url into a subdirectory under base_dir named repo_name.
    If the directory already exists, it is removed first.
    Returns the path to the cloned repository.
    """
    repo_path = os.path.join(base_dir, repo_name)
    # if os.path.exists(repo_path):
    # shutil.rmtree(repo_path)
    # git.Repo.clone_from(repo_url, repo_path, branch=branch)
    return repo_path


def filterFiles(data):
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
    return changed_code_files
