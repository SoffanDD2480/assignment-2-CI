#!/usr/bin/env python3
import json
import os
import subprocess
import argparse
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv

load_dotenv()


def trigger_webhook(
    branch: str = "main",
    name: str = "yourname",
    email: str = "email@gmail.com",
    added: Optional[List[str]] = None,
    modified: Optional[List[str]] = None,
    removed: Optional[List[str]] = None,
) -> None:
    """
    Triggers a webhook to the CI server with the specified parameters.

    Args:
        branch (str): Git branch name (default: "main")
        name (str): Pusher's name (default: "yourname")
        email (str): Pusher's email (default: "email@gmail.com")
        added (list): List of added files (default: [])
        modified (list): List of modified files (default: ["CI_CD_server/app.py"])
        removed (list): List of removed files (default: [])
    """
    if added is None:
        added = []
    if modified is None:
        modified = ["CI_CD_server/app.py"]
    if removed is None:
        removed = []

    payload: Dict[str, Any] = {
        "ref": f"refs/heads/{branch}",
        "pusher": {"name": name, "email": email},
        "commits": [{"added": added, "modified": modified, "removed": removed}],
    }

    payload_json: str = json.dumps(payload)

    # Fix for the "None" error by adding a null check
    webhook_url = os.getenv("CI_CD_SERVER_WEBHOOK_URL")
    if webhook_url is None:
        webhook_url = "http://localhost:8080"  # Default fallback URL
        print(
            "Warning: CI_CD_SERVER_WEBHOOK_URL not set in .env file, using default URL"
        )

    curl_command: List[str] = [
        "curl",
        "-X",
        "POST",
        webhook_url + "/webhook",
        "-H",
        "X-Github-Event: push",
        "-H",
        "Content-Type: application/json",
        "-d",
        payload_json,
    ]

    print("Executing webhook request...")
    try:
        result: subprocess.CompletedProcess = subprocess.run(
            curl_command, capture_output=True, text=True, check=True
        )
        print("Response status:", result.returncode)
        print("Response body:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Trigger CI webhook"
    )
    parser.add_argument("--branch", default="main", help="Git branch name")
    parser.add_argument("--name", default="yourname", help="Pusher's name")
    parser.add_argument("--email", default="email@gmail.com", help="Pusher's email")
    parser.add_argument("--added", nargs="*", default=[], help="List of added files")
    parser.add_argument(
        "--modified",
        nargs="*",
        default=["CI_CD_server/app.py"],
        help="List of modified files",
    )
    parser.add_argument(
        "--removed", nargs="*", default=[], help="List of removed files"
    )

    args: argparse.Namespace = parser.parse_args()

    trigger_webhook(
        branch=args.branch,
        name=args.name,
        email=args.email,
        added=args.added,
        modified=args.modified,
        removed=args.removed,
    )
