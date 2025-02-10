from flask import Flask, request, jsonify
import git
import json
from syntaxCheck import check_syntax
from tests import test


app = Flask(__name__)

directory = "./sample_dir/"


@app.route('/webhook', methods=['POST'])
def webhook():
    msg = []
    if "X-Github-Event" in request.headers and request.headers["X-Github-Event"] == "push":
        data = json.loads(json.dumps(request.json))
        currentBranch = data["ref"].split("/")[-1]  # Get branch
        git.Repo.clone_from("https://github.com/SoffanDD2480/assignment-2-CI.git",
                directory, branch=currentBranch)  # Clone branch repository to sample directory
        syntax_check_results = check_syntax(directory + "assignment-2-CI/code/")
        if not syntax_check_results:
            msg.append("Message about syntax error")
        else:
            msg.append("Successfull syntax check")
            unittest_results = test(directory + "assignment-2-CI/code/")
            if not unittest_results:
                msg.append("Message about test error")
            else:
                msg.append("Successfull test run")

    else:
        return

if __name__ == '__main__':
    app.run(debug=False)
