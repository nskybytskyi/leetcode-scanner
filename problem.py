# Developed with assistance from ChatGPT
import requests
from dataclasses import dataclass
from typing import Iterator


@dataclass
class LeetCodeProblem:
    id: int
    title: str
    slug: str
    difficulty: str
    total_acs: int
    total_submitted: int
    paid_only: bool


def fetch_all_problems() -> Iterator[LeetCodeProblem]:
    """
    Fetches the list of all LeetCode algorithm problems as an iterable.
    Yields:
        LeetCodeProblem instances one by one.
    """
    url = "https://leetcode.com/api/problems/algorithms/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    for pair in data.get("stat_status_pairs", []):
        stat = pair.get("stat", {})
        difficulty_level = pair.get("difficulty", {}).get("level", 0)
        difficulty = {1: "Easy", 2: "Medium", 3: "Hard"}.get(
            difficulty_level, "Unknown"
        )

        yield LeetCodeProblem(
            id=stat.get("question_id"),
            title=stat.get("question__title"),
            slug=stat.get("question__title_slug"),
            difficulty=difficulty,
            total_acs=stat.get("total_acs"),
            total_submitted=stat.get("total_submitted"),
            paid_only=pair.get("paid_only", False),
        )


# Example usage:
if __name__ == "__main__":
    for problem in fetch_all_problems():
        print(problem)
        break  # Only print the first problem for demonstration
