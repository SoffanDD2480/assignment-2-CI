import os


class EmailConfig:
    """Configuration settings for email notifications.

    This class defines the configuration settings needed for sending email
    notifications from the CI/CD server.
    """

    # SMTP settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587  # TLS SMTP port

    # Sender configuration
    DEFAULT_SENDER_EMAIL = "soffan.dd2480@gmail.com"

    @staticmethod
    def get_email_password():
        """
        Get email password from environment variables.

        Returns:
            str: Email password from environment, or None if not set
        """
        return os.getenv("EMAIL_PASSWORD")
