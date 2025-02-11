from flask import Flask, request, jsonify
import git
import json
from syntaxCheck import check_syntax
from tests import test
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime


app = Flask(__name__)

directory = "./sample_dir/"


@app.route('/webhook', methods=['POST'])
def webhook():
    if "X-Github-Event" in request.headers and request.headers["X-Github-Event"] == "push":
        try:
            data = json.loads(json.dumps(request.json))
            currentBranch = data["ref"].split("/")[-1]
            pusher = data["pusher"]["name"], data["pusher"]["email"]
            email_response = Response(pusher, currentBranch)
            git.Repo.clone_from("https://github.com/SoffanDD2480/assignment-2-CI.git",
                    directory, branch=currentBranch)  # Clone branch repository to sample directory
            syntax_check_results = check_syntax(directory + "assignment-2-CI/code/")
            if not syntax_check_results:
                email_response.append_content("Syntax Error Found")
            else:
                email_response.append_content("Successfull syntax check")
                unittest_results = test(directory + "assignment-2-CI/code/")
                if not unittest_results:
                    email_response.append_content("Message about failed tests")
                else:
                    email_response.append_content("Successfull test run")
            email_response.make_response()
            email_response.send_response()
        except Exception as e:
            return

    else:
        return




class Response:
    def __init__(self,
                 pusher: tuple,
                 branch: str
                 ):
        self.response = MIMEMultipart()
        self.timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.NAME_RECEIVER = pusher[0]
        self.EMAIL_RECEIVER = pusher[1]
        self.EMAIL_SENDER = "soffan.dd2480@gmail.com"
        self.EMAIL_PASSWORD = "tmow ikby gdva drcm"
        self.EMAIL_SUBJECT = f"Results from recent push to branch \"{branch}\" at {self.timestamp}."
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587  # TLS SMTP port
        self.body = [f"Greetings {self.NAME_RECEIVER}\n\nHere are the results from your latest push "]

    def append_content(self, info):
        self.body.append(info)

    def make_response(self):
        self.response["From"] = self.EMAIL_SENDER
        self.response["To"] = self.EMAIL_RECEIVER
        self.response["subject"] = self.EMAIL_SUBJECT
        body = ""
        for info in self.body:
            body += "\n\n" + str(info)
        body += "\n\nBest Regards,\nSoffan Team"
        self.response.attach(MIMEText(body, "plain"))

    def send_response(self):
        try:
            server = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            server.starttls()
            server.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            server.sendmail(self.EMAIL_SENDER, self.EMAIL_RECEIVER, self.response.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
        return


if __name__ == '__main__':
    #app.run(debug=False)