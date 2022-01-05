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
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SUBMISSION_URL}{handle}") as r:
                if not r.ok:
                    return None
                data = await r.json()
                return data["result"]
