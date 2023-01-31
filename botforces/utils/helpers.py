"""
Contains helper functions that perform essential tasks for cogs.
Unlike utils/services.py, these functions are used to perform larger chunks of code.
The purpose of this file is refactoring and code reusability, and to avoid cluttering the cogs.
"""


import random

from botforces.utils.api import get_user_submissions
from botforces.utils.db import get_handle_from_db


async def get_unsolved_problems(
    ctx, discord_ids, problems, num_problems=1, handles_provided=False
):
    """
    Returns <num_problems> unsolved problems for the users in discord_ids.
    """

    # discord_ids is a list of Discord IDs sent to the function. The goal is to return problems
    # that are unsolved by all the users in the list.
    for discord_id in discord_ids:
        # Obtain the corresponding Codeforces handle from the database
        # Note: If handles_provided is True, then discord_id is actually a handle, not a Discord ID.
        # This is used in duels, where the user's handle is provided as an argument.
        handle = (
            await get_handle_from_db(discord_id) if not handles_provided else discord_id
        )

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
