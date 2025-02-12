import pytest
import os
from unittest.mock import patch, MagicMock
from compilation import CompilationCheck  # Import the class to test

# A fixture is a function that is called before a test function to set up some test data.
@pytest.fixture
def create_test_files():
    """These two file are created for testing purposes, one is valid and the other is invalid."""
    valid_file = "valid.py"
    invalid_file = "invalid.py"

    # This test file contains a valid Python script
    with open(valid_file, "w") as f:
        f.write("print('Hello, world!')\n") 

    # This test file contains an invalid Python script
    with open(invalid_file, "w") as f:
        f.write("def say_hello()\n    print('Hello')")  

    # We use yield instead of return to return multiple values
    yield valid_file, invalid_file 

    # Cleanup after tests
    for file in [valid_file, invalid_file]:
        if os.path.exists(file):
            os.remove(file)


"""
Structure of the test functions:
The functions below are used to test the CompilationCheck class with different scenarios.
The @patch decorator is used to mock the subprocess.run function, which is used to run the pylint command.
The mock_run parameter is used to replace the subprocess.run function with a MagicMock object.
 -> Magic Object is used to replace the return value of a function, in order to test the function.
Inside the checker object we save the results of the syntax_control method.
The assert statement is used to check if the results are equal to the expected value.
"""

@patch("subprocess.run")
def test_valid_syntax(mock_run, create_test_files):
    """Test with valid Python file that passes the syntax check."""
    valid_file, _ = create_test_files
    # MagicMock is used to create a mock object that can be used to replace the return value of a function, in order to test the function.
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    checker = CompilationCheck(valid_file)
    assert checker.results is True

@patch("subprocess.run")
def test_invalid_syntax(mock_run, create_test_files):
    """Test that an invalid Python file fails the syntax check."""
    _, invalid_file = create_test_files
    mock_run.return_value = MagicMock(returncode=2, stdout="E0001: syntax-error", stderr="")

    checker = CompilationCheck(invalid_file)
    assert checker.results is False

def test_nonexistent_file():
    """Test with non-existent file."""
    checker = CompilationCheck("not_exist.py")
    assert checker.results is False


@patch("subprocess.run", side_effect=FileNotFoundError)
def test_pylint_not_installed(mock_run, create_test_files):
    """Test with an existing file but pylint is not installed."""
    valid_file, _ = create_test_files
    checker = CompilationCheck(valid_file)
    assert checker.results is False
