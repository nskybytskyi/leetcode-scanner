# Developed with assistance from ChatGPT
import requests
import os
import logging
from typing import Iterator, Optional
from problem import LeetCodeProblem
from fetch import fetch_all_problems, fetch_user_submissions
from submission import LeetCodeSubmission


def filter_latest_accepted_python(
    username: str, session: requests.Session
) -> Iterator[tuple[LeetCodeProblem, LeetCodeSubmission]]:
    """
    Loops over all problems and fetches submissions, yielding only the latest accepted Python3 submission per problem.

    Args:
        username (str): The LeetCode username.
        session (requests.Session): An authenticated session.

    Yields:
        LeetCodeSubmission: The latest accepted Python3 submission for each problem.
    """
    for problem in fetch_all_problems():
        latest_submission: Optional[LeetCodeSubmission] = None

        try:
            for submission in fetch_user_submissions(problem.slug, session):
                if submission.status == "Accepted" and submission.lang == "python3":
                    if (
                        latest_submission is None
                        or submission.timestamp > latest_submission.timestamp
                    ):
                        latest_submission = submission
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                logging.warning(
                    f"Skipping paid-only problem: {problem.slug} (403 Forbidden)"
                )
            else:
                logging.error(
                    f"Unexpected error fetching submissions for {problem.slug}: {e}"
                )
            continue  # Move to the next problem

        if latest_submission:
            yield problem, latest_submission


# Example usage
if __name__ == "__main__":
    leetcode_session = os.getenv("LEETCODE_SESSION")

    if not leetcode_session:
        logging.error("The LEETCODE_SESSION environment variable is not set.")
        logging.info("Please export it in your shell:")
        logging.info('   export LEETCODE_SESSION="your_session_cookie"')
        exit(1)

    session = requests.Session()
    session.cookies.set("LEETCODE_SESSION", leetcode_session)

    username = "nika-skybytskyka"

    for submission in filter_latest_accepted_python(username, session):
        print(submission)
        break  # Only print the first submission for demonstration
