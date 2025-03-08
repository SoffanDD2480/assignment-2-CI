# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from pathlib import Path
import sys
import os

# Get the docs directory
DOCS_DIR = Path(__file__).parent.parent
# Get the project root directory (assuming docs is at the project root)
PROJECT_ROOT = DOCS_DIR.parent
# Ensure Sphinx can find your code
# sys.path.insert(0, str(PROJECT_ROOT))

ci_cd_server_path = os.path.join(PROJECT_ROOT, "CI_CD_server")
if os.path.isdir(ci_cd_server_path):
    sys.path.insert(0, ci_cd_server_path)

# -- Project information -----------------------------------------------------
project = "CI/CD"
copyright = (
    "2025, Albin W Woxnerud, Riccardo Coco, Elias Bosæus Fröde and Dmitry Chirin"
)
author = "Albin W Woxnerud, Riccardo Coco, Elias Bosæus Fröde and Dmitry Chirin"
release = "0.2"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Support for Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # Adds links to highlighted source code
    "sphinx.ext.autosummary",  # Generate autodoc summaries
]

autosummary_generate = True  # Enable automatic module summary

autodoc_default_options = {
    "members": True,  # Include class members (functions, variables)
    "undoc-members": True,  # Include members without docstrings
    "show-inheritance": True,  # Show class inheritance hierarchy
    "special-members": "__init__",  # Document __init__ method
    "inherited-members": False,  # Exclude inherited methods
    "noindex": True,  # Prevent duplicate object descriptions
}

# Avoid errors if _static folder does not exist
templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
# Comment out or remove this if the _static directory does not exist
# html_static_path = ["_static"]

autodoc_mock_imports = [
    "sqlalchemy",
    "GitPython",
    "pytest",
    "pylint",
    "black",
    "python_dotenv",
    "flask",
    "sphinxcontrib_napoleon",
    "requests",
    "flask_sqlalchemy",
]
