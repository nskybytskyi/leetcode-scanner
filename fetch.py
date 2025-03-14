import logging
import requests
import time
import unittest

from typing import Iterable
from unittest.mock import Mock

from submission import LeetCodeSubmission
from problem import LeetCodeProblem


def fetch_all_problems() -> Iterable[LeetCodeProblem]:
    """
    Fetches the list of all LeetCode algorithm problems as an iterable.
    Yields:
        LeetCodeProblem instances one by one.
    """
    url = "https://leetcode.com/api/problems/algorithms/"
    response = requests.get(url)
    response.raise_for_status()
    problems = response.json().get("stat_status_pairs")
    yield from map(LeetCodeProblem.from_api_response, problems)


def fetch_problem_submissions(
    problem_slug: str, session: requests.Session
) -> Iterable[LeetCodeSubmission]:
    """Fetches all submissions for a given problem, retrying on 403 and 429 errors."""
    url = f"https://leetcode.com/api/submissions/{problem_slug}/"
    retries = 3  # Maximum retries on failure

    for attempt in range(retries):
        response = session.get(url)
        if response.status_code == 200:
            break  # Success, exit retry loop
        elif response.status_code in {403, 429}:
            logging.warning(
                f"Received {response.status_code} for {problem_slug}, retrying in {5 * (attempt + 1)} seconds..."
            )
            time.sleep(5 * (attempt + 1))
        else:
            logging.error(
                f"Unexpected HTTP error for {problem_slug}: {response.status_code}"
            )
            return
    else:
        logging.error(
            f"Failed to fetch submissions for {problem_slug} after {retries} retries."
        )
        return

    response.raise_for_status()
    data = response.json()
    submissions = data.get("submissions_dump", [])

    for submission in submissions:
        yield LeetCodeSubmission.from_api_response(submission)


def fetch_all_submissions(
    session: requests.Session,
) -> Iterable[tuple[LeetCodeProblem, LeetCodeSubmission]]:
    """
    Fetches all submissions for each problem available on LeetCode.

    Args:
        session (requests.Session): An authenticated session.

    Yields:
        Tuple[LeetCodeProblem, LeetCodeSubmission]: Problem and its corresponding submission.
    """
    for problem in fetch_all_problems():
        try:
            for submission in fetch_problem_submissions(problem.slug, session):
                yield problem, submission
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


class TestFetchUserSubmissions(unittest.TestCase):
    def test_fetch_problem_submissions_mock(self):
        session = Mock()
        session.get.return_value.status_code = 200
        session.get.return_value.json.return_value = {
            "submissions_dump": [
                {
                    "id": 965235677,
                    "question_id": 1,
                    "lang": "cpp",
                    "lang_name": "C++",
                    "time": "1 year, 9 months",
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
                },
            ]
        }
        submissions = list(fetch_problem_submissions("two-sum", session))
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0].problem_slug, "two-sum")
        self.assertEqual(submissions[0].status, "Accepted")
        self.assertEqual(submissions[0].lang, "cpp")
        self.assertEqual(submissions[0].code, "int main() { return 0; }")


if __name__ == "__main__":
    unittest.main()
