from pathlib import Path
from setuptools import setup, find_packages
import os
import sys

current_dir = Path(__file__).resolve().parent
requirements_file = current_dir / "requirements.txt"


def get_requirements() -> list[str]:
    with open(requirements_file) as f:
        requirements = f.read().splitlines()
    return requirements


# Check for .env file and provide instructions if missing
env_file = current_dir / ".env"
if not env_file.exists():
    print("WARNING: .env file is required but was not found.", file=sys.stderr)
    print("Please create a .env file with EMAIL_PASSWORD defined.", file=sys.stderr)
    print("Example: EMAIL_PASSWORD=your_email_password", file=sys.stderr)


# Configuration for setup
setup_args = {
    "name": "assignment-2-CI",
    "version": "0.1.0",
    "description": "Continuous Integration assignment",
    "author": "Albin W Woxnerud, Riccardo Coco, Elias Bosæus Fröde and Dmitry Chirin",
    "author_email": "soffan.dd2480@gmail.com",
    "packages": find_packages(),
    "install_requires": get_requirements(),
    "python_requires": ">=3.12",
    "classifiers": [
        "Development Status :: 2 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    "long_description": """
    This package requires a .env file in the root directory with EMAIL_PASSWORD defined.
    Example:
    EMAIL_PASSWORD=your_email_password

    Without this file, the application will encounter errors during execution.
    """,
}

if __name__ == "__main__":
    setup(**setup_args)
