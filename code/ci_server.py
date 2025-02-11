from flask import Flask, request, jsonify
import git
import json
from syntaxCheck import check_syntax
from tests import test
from email_response import Response


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
        except:
            return
    else:
        return


if __name__ == '__main__':
    app.run(debug=False)