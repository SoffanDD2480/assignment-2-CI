import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime

from CI_CD_server.src.config.email_config import EmailConfig


class Response:
    def __init__(self, pusher: tuple, branch: str) -> None:
        """
        Initialize a new email response object.

        Args:
            pusher (tuple): A tuple containing (name, email) of the person who pushed the changes
            branch (str): The name of the branch where changes were pushed

        Attributes:
            response (MIMEMultipart): The email message object
            timestamp (str): Current timestamp in 'YYYY-MM-DD HH:MM:SS' format
            NAME_RECEIVER (str): Name of the person who pushed the changes
            EMAIL_RECEIVER (str): Email of the person who pushed the changes
            EMAIL_SENDER (str): Email address used to send notifications (from config)
            EMAIL_PASSWORD (str): Password for the sender email (from environment variables)
            EMAIL_SUBJECT (str): Subject line of the email
            SMTP_SERVER (str): SMTP server address (from config)
            SMTP_PORT (int): SMTP server port number (from config)
            body (list): List of strings containing the email body content

        Example:
            >>> pusher = ("John Doe", "john@example.com")
            >>> email_response = Response(pusher, "main")
            >>> email_response.append_content("Tests passed successfully")
            >>> email_response.make_response()
            >>> email_response.send_response()
        """
        self.response = MIMEMultipart()
        self.timestamp = datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.NAME_RECEIVER = pusher[0]
        self.EMAIL_RECEIVER = pusher[1]
        self.EMAIL_SENDER = EmailConfig.DEFAULT_SENDER_EMAIL
        self.EMAIL_PASSWORD = EmailConfig.get_email_password()
        self.EMAIL_SUBJECT = (
            f'Results from recent push to branch "{branch}" at {self.timestamp}.'
        )
        self.SMTP_SERVER = EmailConfig.SMTP_SERVER
        self.SMTP_PORT = EmailConfig.SMTP_PORT
        self.intro = f"Greetings {self.NAME_RECEIVER}\n\nHere are the results from your latest push:\n\n"
        self.body: list[str] = []
        self.passed_syntax = True
        self.passed_tests = True

    # Rest of the class remains unchanged
    def append_content(self, info: str) -> None:
        """
        Append new content to the email body.

        Args:
            info (str): The information to be added to the email body

         Example:
            >>> email_response.append_content("All tests passed")
            >>> email_response.append_content("Code formatting successful")
        """
        self.body.append(info)

    def make_response(self) -> None:
        """
        Construct the email message with headers and body.

        Combines all the content in self.body into a single email message,
        adds headers (From, To, Subject), and attaches the body text.

        Example:
            >>> email_response.append_content("Build successful")
            >>> email_response.make_response()  # Prepares email for sending
        """

        self.response["From"] = self.EMAIL_SENDER
        self.response["To"] = self.EMAIL_RECEIVER
        self.response["Subject"] = self.EMAIL_SUBJECT
        body = self.intro
        if self.passed_syntax:
            body += "✅ SYNTAX CHECK PASSED\n"
        else:
            body += "❌ SYNTAX CHECK FAILED\n"

        if self.passed_tests:
            body += "✅ ALL TESTS PASSED\n"
        else:
            body += "❌ SOME TESTS FAILED\n"

        body += "\nSee details below:"
        for info in self.body:
            body += "\n\n" + str(info)
        if not (self.passed_syntax and self.passed_tests):
            body += (
                "\n\nFor further details, please consult server log.\n"
                "Please fix the above issues as soon as possible"
            )
        else:
            body += "\n\nSyntax Check + All tests passed! Code is good to go"
        body += "\n\nBest Regards,\nTeam Soffan"
        self.response.attach(MIMEText(body, "plain"))

    def set_syntax_result(self, result: bool) -> None:
        """
        Set the syntax check result.

        Args:
            result (bool): True if syntax check passed, False otherwise

        Example:
            >>> email_response.set_syntax_result(False)
        """
        self.passed_syntax = result

    def set_tests_result(self, result: bool) -> None:
        """
        Set the test results.

        Args:
            result (bool): True if all tests passed, False otherwise

        Example:
            >>> email_response.set_tests_result(False)
        """
        self.passed_tests = result

    def send_response(self) -> None:
        """
        Send the email using SMTP with TLS.

        Establishes a connection to the SMTP server, authenticates using the
        provided credentials, sends the email, and closes the connection.

        Raises:
            Exception: If there is an error during the email sending process
        Example:
            >>> try:
            ...     email_response.send_response()
            ... except Exception as e:
            ...     print(f"Failed to send email: {e}")
        """

        if not self.EMAIL_PASSWORD:
            raise ValueError("Email password not configured or is None")

        try:
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()
            server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            server.sendmail(
                self.EMAIL_SENDER, self.EMAIL_RECEIVER, self.response.as_string()
            )
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            raise
