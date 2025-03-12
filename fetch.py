import requests
from typing import Iterable
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
