# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Ensure Sphinx can find your code
sys.path.insert(0, os.path.abspath("../../code"))

# -- Project information -----------------------------------------------------
project = "CI/CD"
copyright = "2025, Albin W Woxnerud, Riccardo, Elias, Dima"
author = "Albin W Woxnerud, Riccardo, Elias, Dima"
release = "0.1"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Support for Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # Adds links to highlighted source code
]

autodoc_default_options = {
    "members": True,  # Include class members (functions, variables)
    "undoc-members": True,  # Include members without docstrings
    "show-inheritance": True,  # Show class inheritance hierarchy
    "special-members": "__init__",  # Document __init__ method
    "inherited-members": True,  # Include inherited methods
    "noindex": True,  # Prevent duplicate object descriptions
}

# Avoid errors if _static folder does not exist
templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
# Comment out or remove this if the _static directory does not exist
# html_static_path = ["_static"]
