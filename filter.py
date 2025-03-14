import unittest
from typing import Iterable, Optional
from submission import LeetCodeSubmission
from problem import LeetCodeProblem


def filter_latest_submissions(
    submissions: Iterable[tuple[LeetCodeProblem, LeetCodeSubmission]],
    language: Optional[str],
    status: Optional[str],
) -> Iterable[tuple[LeetCodeProblem, LeetCodeSubmission]]:
    """
    Filters the latest submission for each problem based on language and status.

    Args:
        submissions (Iterable[tuple[LeetCodeProblem, LeetCodeSubmission]]): Submissions to filter.
        language (str): Programming language to filter by (default: "python3").
        status (str): Submission status to filter by (default: "Accepted").

    Yields:
        tuple[LeetCodeProblem, LeetCodeSubmission]: Problem and its latest submission matching the criteria.
    """
    latest_submissions = {}

    for problem, submission in submissions:
        if (
            (status is None or submission.status == status)
            and (language is None or submission.lang == language)
            and (
                problem not in latest_submissions
                or submission.timestamp > latest_submissions[problem].timestamp
            )
        ):
            latest_submissions[problem] = submission

    yield from latest_submissions.items()


class TestFilterSubmissions(unittest.TestCase):
    def setUp(self):
        self.problem = LeetCodeProblem(
            id=1, title="Two Sum", slug="two-sum", paid_only=False
        )
        submissions = [
            LeetCodeSubmission(
                id=1,
                problem_slug="two-sum",
                status="Wrong Answer",
                lang="python3",
                timestamp=1000,
                code="print(1)",
            ),
            LeetCodeSubmission(
                id=2,
                problem_slug="two-sum",
                status="Accepted",
                lang="python3",
                timestamp=2000,
                code="print(2)",
            ),
            LeetCodeSubmission(
                id=3,
                problem_slug="three-sum",
                status="Accepted",
                lang="cpp",
                timestamp=3000,
                code="std::cout << 3;",
            ),
            LeetCodeSubmission(
                id=4,
                problem_slug="four-sum",
                status="Accepted",
                lang="python3",
                timestamp=4000,
                code="print(4)",
            ),
        ]
        self.submissions = [(self.problem, submission) for submission in submissions]

    def test_filter_latest_accepted_python_submission(self):
        result = list(
            filter_latest_submissions(
                self.submissions, language="python3", status="Accepted"
            )
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1].id, 4)  # Latest accepted Python3 submission

    def test_no_matching_submissions(self):
        result = list(
            filter_latest_submissions(
                self.submissions, language="java", status="Accepted"
            )
        )
        self.assertEqual(len(result), 0)  # No Java submissions

    def test_filter_by_status_only(self):
        result = list(
            filter_latest_submissions(
                self.submissions, language=None, status="Accepted"
            )
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1].id, 4)  # Latest accepted in any language

    def test_filter_by_language_only(self):
        result = list(
            filter_latest_submissions(self.submissions, language="cpp", status=None)
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1].id, 3)  # Latest C++ submission


if __name__ == "__main__":
    unittest.main()
