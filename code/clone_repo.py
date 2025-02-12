import git
import os
import shutil

def clone_repo(directory: str,
               currentBranch: str,
               ):
    if not os.path.exists(directory):
        git.Repo.clone_from("https://github.com/SoffanDD2480/assignment-2-CI.git",
                            directory, branch=currentBranch)
    else:
        shutil.rmtree(directory)
        git.Repo.clone_from("https://github.com/SoffanDD2480/assignment-2-CI.git",
                            directory, branch=currentBranch)