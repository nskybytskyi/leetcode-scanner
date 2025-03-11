# Developed with assistance from ChatGPT
import os
import subprocess
import requests
from submission import LeetCodeSubmission, fetch_user_submissions
from problem import LeetCodeProblem, fetch_all_problems
from filter import filter_latest_accepted_python
from format import save_and_commit_submission


def main(username: str) -> None:
    """Main function to scan user submissions and make git commits."""
    # Initialize Git repository (if not already initialized)
    if not os.path.isdir(".git"):
        subprocess.run(["git", "init"], check=True)
        print("Git repository initialized.")

    # Create a session with the LEETCODE_SESSION environment variable
    session = requests.Session()
    session.cookies.set("LEETCODE_SESSION", os.getenv("LEETCODE_SESSION"))

    # Get filtered list of latest accepted Python submissions
    for problem, submission in filter_latest_accepted_python(username, session):
        # Save and commit each accepted Python submission
        save_and_commit_submission((problem, submission))

    # Push all commits to the repository
    subprocess.run(["git", "push"], check=True)
    print("Pushed all commits to the repository.")


# Example usage:
if __name__ == "__main__":
    # Assuming you have set the LEETCODE_SESSION environment variable and want to scan a specific user's submissions
    username = "nika-skybytska"  # Replace with your actual LeetCode username
    main(username)
