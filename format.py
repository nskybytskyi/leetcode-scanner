# Developed with assistance from ChatGPT
import os
import autopep8
import subprocess
from typing import Tuple
from submission import LeetCodeSubmission
from problem import LeetCodeProblem


def save_submission_to_file(
    problem_submission_pair: Tuple[LeetCodeProblem, LeetCodeSubmission],
) -> None:
    """
    Saves the Python code of a given submission to a file in the current directory.
    The filename is based on the problem ID and slug, and the code is automatically
    reformatted according to PEP8.

    Args:
        problem_submission_pair (Tuple[LeetCodeProblem, LeetCodeSubmission]): A tuple of
        LeetCodeProblem and LeetCodeSubmission instances.
    """
    problem, submission = problem_submission_pair
    problem_id = f"{problem.id:04d}"  # Zero-padded to 4 digits
    filename = f"{problem_id}-{problem.slug}.py"

    # Reformat the code using autopep8 to ensure it adheres to PEP8
    formatted_code = autopep8.fix_code(submission.code)

    # Create and write the code to the file
    with open(filename, "w") as file:
        file.write(formatted_code)

    print(f"Submission code saved to {filename}")


def save_and_commit_submission(
    problem_submission_pair: Tuple[LeetCodeProblem, LeetCodeSubmission],
) -> None:
    """
    Saves the submission code to a file and commits it to a git repository using
    the submission timestamp as the commit date.

    Args:
        problem_submission_pair (Tuple[LeetCodeProblem, LeetCodeSubmission]): A tuple of
        LeetCodeProblem and LeetCodeSubmission instances.
    """
    # Save the submission code to a file
    save_submission_to_file(problem_submission_pair)

    # Extract the timestamp from the submission and format it
    submission = problem_submission_pair[1]
    timestamp = submission.timestamp
    commit_message = f"LeetCode submission: {submission.problem_slug}"

    # Run Git commands to add the file, commit it, and set the commit date
    filename = (
        f"{problem_submission_pair[0].id:04d}-{problem_submission_pair[0].slug}.py"
    )

    # Format the timestamp as "Wed Jan  1 00:00:00 2021"
    commit_date = subprocess.run(
        ["date", "-r", str(timestamp), "+%a %b %d %H:%M:%S %Y"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    try:
        # Add the file to the staging area
        subprocess.run(["git", "add", filename], check=True)

        # Commit with a custom date (commit date will be the timestamp from submission)
        subprocess.run(
            ["git", "commit", "--date", commit_date, "-m", commit_message],
            check=True,
        )
        print(f"Successfully committed: {commit_message} at {commit_date}")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")


# Example usage:
if __name__ == "__main__":
    # Assuming you have an existing problem and submission pair
    problem = LeetCodeProblem(
        id=1,
        title="Two Sum",
        slug="two-sum",
        difficulty="Easy",
        total_acs=0,
        total_submitted=0,
        paid_only=False,
    )

    submission = LeetCodeSubmission(
        submission_id=0,
        timestamp=1609459200,  # Example timestamp: 2021-01-01 00:00:00
        problem_slug="two-sum",
        status="Accepted",
        lang="python3",
        code="""def two_sum(nums, target):
            # Iterate through the list
            for i in range(len(nums)):
                for j in range(i+1, len(nums)):
                    if nums[i] + nums[j] == target:
                        return [i, j]  # Found the solution
        """,
    )

    # Save the submission and commit it
    save_and_commit_submission((problem, submission))
