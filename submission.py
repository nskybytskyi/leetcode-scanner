# Developed with assistance from ChatGPT
import requests
import time
import logging
from typing import Iterator


class LeetCodeSubmission:
    """Represents a single LeetCode submission."""

    def __init__(
        self,
        submission_id: int,
        problem_slug: str,
        status: str,
        lang: str,
        timestamp: int,
        code: str,
    ):
        self.submission_id = submission_id
        self.problem_slug = problem_slug
        self.status = status
        self.lang = lang
        self.timestamp = timestamp
        self.code = code

    def __repr__(self):
        return f"<LeetCodeSubmission {self.problem_slug} ({self.lang}, {self.status})>"


def fetch_user_submissions(
    problem_slug: str, username: str, session: requests.Session
) -> Iterator[LeetCodeSubmission]:
    """
    Fetches all submissions for a given problem, retrying on 403 (forbidden) and 429 (rate-limited).

    Args:
        problem_slug (str): The slug identifier for the problem (e.g., "two-sum").
        username (str): The LeetCode username.
        session (requests.Session): An authenticated session.

    Yields:
        LeetCodeSubmission: A submission object.
    """
    url = f"https://leetcode.com/api/submissions/{problem_slug}/"
    retries = 3  # Retry up to 3 times on 403/429

    headers = {
        "Referer": "https://leetcode.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    for attempt in range(retries):
        response = session.get(url, headers=headers)

        if response.status_code == 429:
            logging.warning(
                f"Rate-limited for problem {problem_slug}, retrying after delay..."
            )
            time.sleep(5 * (attempt + 1))  # Increase delay between retries
            continue
        elif response.status_code == 403:
            if attempt == retries - 1:
                logging.warning(
                    f"Paid-only problem detected: {problem_slug} (403 Forbidden) after {retries} retries."
                )
            else:
                logging.warning(f"Received 403 for {problem_slug}, retrying...")
            time.sleep(5 * (attempt + 1))  # Increase delay between retries
            continue
        elif response.status_code != 200:
            logging.error(
                f"Unexpected HTTP error for {problem_slug}: {response.status_code}"
            )
            break

        response.raise_for_status()  # Raise an error if status is not 200

        data = response.json()
        submissions = data.get("submissions_dump", [])

        for submission in submissions:
            yield LeetCodeSubmission(
                submission_id=submission["id"],
                problem_slug=problem_slug,
                status=submission["status_display"],
                lang=submission["lang"],
                timestamp=submission["timestamp"],
                code=submission["code"],
            )

        break  # Exit the retry loop if successful


# Example usage
if __name__ == "__main__":
    import os

    leetcode_session = os.getenv("LEETCODE_SESSION")

    if not leetcode_session:
        logging.error("The LEETCODE_SESSION environment variable is not set.")
        logging.info("Please export it in your shell:")
        logging.info('   export LEETCODE_SESSION="your_session_cookie"')
        exit(1)

    session = requests.Session()
    session.cookies.set("LEETCODE_SESSION", leetcode_session)

    username = "nika-skybytskyka"
    problem_slug = "two-sum"

    try:
        for submission in fetch_user_submissions(problem_slug, username, session):
            print(submission)
            break  # Only print the first submission for demonstration
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
