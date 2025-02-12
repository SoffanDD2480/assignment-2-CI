import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime
import os


class Response:
    def __init__(self, pusher: tuple, branch: str):
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
            EMAIL_SENDER (str): Email address used to send notifications
            EMAIL_PASSWORD (str): Password for the sender email (from environment variables)
            EMAIL_SUBJECT (str): Subject line of the email
            SMTP_SERVER (str): SMTP server address
            SMTP_PORT (int): SMTP server port number
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
        self.EMAIL_SENDER = "soffan.dd2480@gmail.com"
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.EMAIL_SUBJECT = (
            f'Results from recent push to branch "{branch}" at {self.timestamp}.'
        )
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587  # TLS SMTP port
        self.body = [
            f"Greetings {self.NAME_RECEIVER}\n\nHere are the results from your latest push "
        ]

    def append_content(self, info):
        """
        Append new content to the email body.

        Args:
            info (str): The information to be added to the email body

         Example:
            >>> email_response.append_content("All tests passed")
            >>> email_response.append_content("Code formatting successful")
        """
        self.body.append(info)

    def make_response(self):
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
        body = ""
        for info in self.body:
            body += "\n\n" + str(info)
        body += "\n\nBest Regards,\nTeam Soffan"
        self.response.attach(MIMEText(body, "plain"))

    def send_response(self):
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
