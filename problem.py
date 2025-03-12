from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class LeetCodeProblem:
    """
    Represents a LeetCode problem with essential attributes.

    Attributes:
        id (int): The unique identifier of the problem.
        title (str): The title of the problem.
        slug (str): The URL-friendly slug of the problem.
        paid_only (bool): Indicates whether the problem requires a premium subscription.
    """

    id: int
    title: str
    slug: str
    paid_only: bool

    @classmethod
    def from_api_response(cls, response: dict) -> Self:
        """
        Creates a LeetCodeProblem instance from an API response.

        Args:
            response (dict): The JSON dictionary from LeetCode's API.

        Returns:
            Self: An instance of LeetCodeProblem.
        """
        stat = response["stat"]
        return cls(
            id=stat["question_id"],
            title=stat["question__title"],
            slug=stat["question__title_slug"],
            paid_only=response["paid_only"],
        )


def test_leetcode_problem():
    sample_response = {
        "stat": {
            "question_id": 3825,
            "question__article__live": None,
            "question__article__slug": None,
            "question__article__has_video_solution": None,
            "question__title": "Apply Substitutions",
            "question__title_slug": "apply-substitutions",
            "question__hide": False,
            "total_acs": 227,
            "total_submitted": 254,
            "frontend_question_id": 3481,
            "is_new_question": True,
        },
        "status": None,
        "difficulty": {"level": 2},
        "paid_only": True,
        "is_favor": False,
        "frequency": 0,
        "progress": 0,
    }

    problem = LeetCodeProblem.from_api_response(sample_response)
    assert problem.id == 3825
    assert problem.title == "Apply Substitutions"
    assert problem.slug == "apply-substitutions"
    assert problem.paid_only is True

    print("All tests passed!")


if __name__ == "__main__":
    test_leetcode_problem()
