# Developed with assistance from ChatGPT
import os
import subprocess
import requests

from fetch import fetch_all_submissions
from filter import filter_latest_submissions
from format import save_and_commit_submission


def main() -> None:
    """Main function to scan user submissions and make git commits."""
    # Initialize Git repository (if not already initialized)
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init"], check=True)
        print("Git repository initialized.")

    # Create a session with the LEETCODE_SESSION environment variable
    session = requests.Session()
    session.cookies.set("LEETCODE_SESSION", os.getenv("LEETCODE_SESSION"))

    # Get filtered list of latest accepted Python submissions
    submissions = fetch_all_submissions(session)
    for problem, submission in filter_latest_submissions(
        submissions, language="python3", status="Accepted"
    ):
        # Save and commit each accepted Python submission
        save_and_commit_submission((problem, submission))

    # Push all commits to the repository
    subprocess.run(["git", "push"], check=True)
    print("Pushed all commits to the repository.")


if __name__ == "__main__":
    # Assuming you have set the LEETCODE_SESSION environment variable
    main()
