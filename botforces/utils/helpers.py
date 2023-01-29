"""
Contains helper functions that perform essential tasks for cogs.
Unlike utils/services.py, these functions are used to perform larger chunks of code.
The purpose of this file is refactoring and code reusability, and to avoid cluttering the cogs.
"""


import random

from botforces.utils.api import get_user_submissions
from botforces.utils.db import get_handle_from_db


async def get_unsolved_problems(ctx, discord_id, problems, num_problems=1):
    """
    Returns <num_problems> unsolved problems for the user.
    """

    # Obtain the corresponding Codeforces handle from the database
    handle = await get_handle_from_db(discord_id)

    # If the user has not registered, return random problems
    if handle is None:
        return random.sample(problems, min(num_problems, len(problems)))

    # Obtain the user's submissions from the Codeforces API
    submissions = await get_user_submissions(ctx, handle)

    # Filter out the AC submissions
    submissions = list(
        filter(lambda submission: submission["verdict"] == "OK", submissions)
    )

    # Removethe solved problems from the list of problems
    problems = list(
        filter(
            lambda problem: not any(
                submission["problem"]["contestId"] == problem["contestId"]
                and submission["problem"]["index"] == problem["contestIndex"]
                for submission in submissions
            ),
            problems,
        )
    )

    # If there are no unsolved problems, return None
    if len(problems) == 0:
        return None

    # Return random <num_problems> problems.
    # Note: Why return a list? This is for extensibility. In the future, we might want to return
    # multiple unsolved problems. For example, say I decide to add a lockout match feature, which
    # would require more than one unsolved problem to be returned. This is more efficient than
    # calling a function to return one unsolved problem multiple times.
    return random.sample(problems, min(num_problems, len(problems)))
