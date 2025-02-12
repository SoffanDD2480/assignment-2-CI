import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime
import os


class Response:
    def __init__(self,
                 pusher: tuple,
                 branch: str):
        self.response = MIMEMultipart()
        self.timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.NAME_RECEIVER = pusher[0]
        self.EMAIL_RECEIVER = pusher[1]
        self.EMAIL_SENDER = "soffan.dd2480@gmail.com"
        self.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
        self.EMAIL_SUBJECT = f"Results from recent push to branch \"{branch}\" at {self.timestamp}."
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587  # TLS SMTP port
        self.body = [f"Greetings {self.NAME_RECEIVER}\n\nHere are the results from your latest push "]

    def append_content(self, info):
        self.body.append(info)

    def make_response(self):
        self.response["From"] = self.EMAIL_SENDER
        self.response["To"] = self.EMAIL_RECEIVER
        self.response["Subject"] = self.EMAIL_SUBJECT
        body = ""
        for info in self.body:
            body += "\n\n" + str(info)
        body += "\n\nBest Regards,\nTeam Soffan"
        self.response.attach(MIMEText(body, "plain"))

    def send_response(self):
        try:
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()
            server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            server.sendmail(self.EMAIL_SENDER, self.EMAIL_RECEIVER, self.response.as_string())
            server.quit()
            print("Email sent successfully!", self.EMAIL_RECEIVER)
        except Exception as e:
            print(f"Error sending email: {e}")
            raise