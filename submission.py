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


if __name__ == "__main__":
    unittest.main()
