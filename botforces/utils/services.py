"""
Contains service and utility functions for cogs.
"""


import datetime

from botforces.utils.api import get_user_by_handle
from botforces.utils.constants import PROBLEM_WEBSITE_URL


async def sort_dict_by_value(dictionary, reverse=False):
    """
    Sorts a dictionary by value.
    """

    return dict(sorted(dictionary.items(), key=lambda kv: kv[1], reverse=reverse))


async def map_rank_to_color(rank):
    """
    Maps rank to corresponding color.
    """

    color = 0xFF0000

    if not rank:
        color = 0x000000
    elif rank == "newbie":
        color = 0x918F8E
    elif rank == "pupil":
        color = 0x087515
    elif rank == "specialist":
        color = 0x1AF2F2
    elif rank == "expert":
        color = 0x1300F9
    elif rank == "candidate master":
        color = 0xB936EE
    elif rank == "master" or rank == "international master":
        color = 0xEEBB36

    return color


async def check_tags(problem_tags, tags):
    """
    To check if all tags are present in the problem tags.
    """
    count = 0
    for tag in tags:
        if "'" + tag + "'" in problem_tags:
            count += 1

    return count == len(tags)


async def enclose_tags_in_spoilers(tags):
    """
    Encloses the tags in spoilers and returns the resultant string.
    """

    tags = tags.split(", ")
    tags = [tag.strip("[]'") for tag in tags]
    tags = map(lambda str: "||" + str + "||", tags)
    tags = ",".join(tags)

    return tags


async def verify_handles(ctx, handle_1, handle_2):
    """
    Verifies if the handles are valid.
    """

    if await get_user_by_handle(ctx, handle_1) and await get_user_by_handle(
        ctx, handle_2
    ):
        return True
    else:
        return False


async def separate_rating_and_tags(args):
    """
    Separates out the rating and tags from the arguments.
    """

    rating = 0
    tags = []
    for arg in args:
        if arg.isdigit():
            rating = int(arg)
        else:
            tags.append(arg)

    return rating, tags


async def convert_submissions_to_string(problems, number):
    """
    Takes the last n solved problems and returns the result as a string.
    """

    submissions = ""

    count = 1
    startTime = datetime.datetime.now()

    for problem in problems:
        if "rating" in problem["problem"]:
            rating = problem["problem"]["rating"]
        else:
            rating = "?"

        submissions += f"{count}. [{problem['problem']['name']}]({PROBLEM_WEBSITE_URL}{problem['problem']['contestId']}/{problem['problem']['index']}) - {rating} "
        difference = startTime - datetime.datetime.fromtimestamp(
            int(problem["creationTimeSeconds"])
        )
        if difference.days == 1:
            submissions += "(1 day ago)\n"
        else:
            submissions += f"({difference.days} days ago)\n"

        if count == number:
            break

        count += 1

    return submissions, count


async def decide_verdict(duel, user_submission, opponent_submission):
    """
    Decides the verdict of the last submissions of the users.
    """

    # Boolean variables to check whether both users solved the problem
    user_solved = False
    opponent_solved = False

    # Converting the timestamps to datetime objects
    user_submission["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
        user_submission["creationTimeSeconds"]
    )
    opponent_submission["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
        opponent_submission["creationTimeSeconds"]
    )

    startTime = datetime.datetime.strptime(duel["startTime"], "%Y-%m-%d %H:%M:%S.%f")
    if (
        duel["contestId"] == user_submission["problem"]["contestId"]
        and user_submission["creationTimeSeconds"] > startTime
        and duel["contestIndex"] == user_submission["problem"]["index"]
        and user_submission["verdict"] == "OK"
    ):
        user_solved = True
    if (
        duel["contestId"] == opponent_submission["problem"]["contestId"]
        and opponent_submission["creationTimeSeconds"] > startTime
        and duel["contestIndex"] == opponent_submission["problem"]["index"]
        and opponent_submission["verdict"] == "OK"
    ):
        opponent_solved = True

    return user_solved, opponent_solved
