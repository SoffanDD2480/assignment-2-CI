import pytest
from unittest.mock import patch, MagicMock
import os
from email_response import Response 

"""
This test file is used to test the Response class in email_response.py. 
The Response class is used to send an email to the pusher of a branch with the results of the tests.
The tests check the following:
    - Initialization of the Response class
    - Appending content to the email body
    - Constructing the email message
    - Sending the email message
"""

@pytest.fixture
def response():
    """We use fixture to initialize the Response class with some default values."""
    pusher = ("Marco Carta", "Marco@gmail.com")
    branch = "main"
    return Response(pusher, branch)

def test_initialization(response):
    """Test if the Response class initializes correctly.
    Ensures all attributes are correctly set.
    """
    assert response.NAME_RECEIVER == "Marco Carta"
    assert response.EMAIL_RECEIVER == "Marco@gmail.com"
    assert response.EMAIL_SENDER == "soffan.dd2480@gmail.com"
    assert response.SMTP_SERVER == "smtp.gmail.com"
    assert response.SMTP_PORT == 587
    assert "Greetings Marco Carta" in response.body[0]

def test_append_content(response):
    """Test if content is appended correctly to the email body.
    this test add a string to the email body and check if it is present in the body."""
    response.append_content("Tests passed successfully")
    assert "Tests passed successfully" in response.body

def test_make_response(response):
    """Test if make_response constructs the email properly.
    Ensures that headers (From, To, Subject) are set correctly and that the body.
    """
    response.append_content("All tests passed")
    response.make_response()
    assert response.response["From"] == "soffan.dd2480@gmail.com"
    assert response.response["To"] == "Marco@gmail.com"
    assert "All tests passed" in response.response.get_payload()[0].get_payload()

@patch("smtplib.SMTP")
def test_send_response(mock_smtp, response):
    """Test if send_response successfully sends an email.
    Uses a mock SMTP server to ensure the correct sequence of operations is followed."""
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server
    
    response.EMAIL_PASSWORD = "fakepassword"  # Mocking environment variable
    response.make_response()
    response.send_response()

    mock_smtp.assert_called_with("smtp.gmail.com", 587)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("soffan.dd2480@gmail.com", "fakepassword")
    mock_server.sendmail.assert_called_once()
    mock_server.quit.assert_called_once()
