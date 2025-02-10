import os


# TODO: Implement syntax check function
def check_syntax(path: str):
    if not os.path.exists(path):
        print("Path does not exist")
        return False
    return