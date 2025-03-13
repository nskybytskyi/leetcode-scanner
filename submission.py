from dataclasses import dataclass
from typing import Self
import unittest


@dataclass(frozen=True, slots=True)
class LeetCodeSubmission:
    """
    Represents a LeetCode submission with essential attributes.

    Attributes:
        id (int): The unique identifier of the submission.
        problem_slug (str): The URL-friendly slug of the problem.
        status (str): The user-friendly judgement verdict of the submission.
        lang (str): The programming language of the submission.
        timestamp (int): The judgement time of the submission.
        code (str): The source code of the submission.
    """

    id: int
    problem_slug: str
    status: str
    lang: str
    timestamp: int
    code: str

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        """
        Creates a LeetCodeSubmission instance from an API response.

        Args:
            response (dict): The JSON dictionary from LeetCode's API.

        Returns:
            Self: An instance of LeetCodeSubmission.
        """
        return cls(
            id=response["id"],
            problem_slug=response["title_slug"],
            status=response["status_display"],
            lang=response["lang"],
            timestamp=response["timestamp"],
            code=response["code"],
        )


class TestLeetCodeSubmission(unittest.TestCase):
    def test_from_api_response(self):
        api_response = {
            "id": 965235677,
            "question_id": 1,
            "lang": "cpp",
            "lang_name": "C++",
            "time": "1\xa0year, 9\xa0months",
            "timestamp": 1686064192,
            "status": 10,
            "status_display": "Accepted",
            "runtime": "47 ms",
            "url": "/submissions/detail/965235677/",
            "is_pending": "Not Pending",
            "title": "Two Sum",
            "memory": "11.5 MB",
            "code": "int main() { return 0; }",
            "compare_result": "111111111111111111111111111111111111111111111111111111111",
            "title_slug": "two-sum",
            "has_notes": False,
            "flag_type": 1,
            "frontend_id": 12,
        }
        submission = LeetCodeSubmission.from_api_response(api_response)
        self.assertEqual(submission.id, 965235677)
        self.assertEqual(submission.problem_slug, "two-sum")
        self.assertEqual(submission.status, "Accepted")
        self.assertEqual(submission.lang, "cpp")
        self.assertEqual(submission.timestamp, 1686064192)
        self.assertEqual(submission.code, "int main() { return 0; }")


import requests
import time
import logging
from typing import Iterator


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
            yield LeetCodeSubmission.from_api_response(submission)

        break  # Exit the retry loop if successful


# Example usage
if __name__ == "__main__":
    unittest.main()
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
