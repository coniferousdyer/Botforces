"""
The API module interacts with the Codeforces API, obtaining real-time data about user, problem and contest statistics.
"""


import aiohttp

from botforces.utils.constants import USER_URL, CONTEST_URL, PROBLEM_URL, SUBMISSION_URL


async def get_user_by_handle(ctx, handle):
    """
    Gets user information from the Codeforces API.
    """

    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{USER_URL}{handle}") as r:
                if not r.ok:
                    return None
                data = await r.json()
                return data["result"][0]


async def get_all_upcoming_contests():
    """
    Gets all upcoming contests from the Codeforces API.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(CONTEST_URL) as r:
            data = await r.json()
            return data["result"]


async def get_all_problems():
    """
    Gets all rated problems from the Codeforces API.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(PROBLEM_URL) as r:
            data = await r.json()
            data["result"]["problems"] = filter(
                lambda p: "rating" in p, data["result"]["problems"]
            )
            return data["result"]["problems"]


async def get_user_submissions(ctx, handle):
    """
    Gets all submissions of a user from the Codeforces API.
    """

    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SUBMISSION_URL}{handle}") as r:
                if not r.ok:
                    return None
                data = await r.json()
                return data["result"]


async def get_users_last_submission(ctx, duel):
    """
    Gets the last submission of the users from the Codeforces API.
    """
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{SUBMISSION_URL}{duel['handle_1']}&from=1&count=1"
            ) as r1:
                async with session.get(
                    f"{SUBMISSION_URL}{duel['handle_2']}&from=1&count=1"
                ) as r2:
                    data_1 = await r1.json()
                    data_2 = await r2.json()

    return data_1["result"][0], data_2["result"][0]
