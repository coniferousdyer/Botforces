"""
Service functions for cogs.
"""

import datetime

from botforces.utils.constants import PROBLEM_WEBSITE_URL


def sort_dict_by_value(dictionary, reverse=False):
    """
    Sorts a dictionary by value.
    """

    return dict(sorted(dictionary.items(), key=lambda kv: kv[1], reverse=reverse))


def map_rank_to_color(rank):
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


def check_tags(problem_tags, tags):
    """
    To check if all tags are present in the problem tags.
    """
    count = 0
    for tag in tags:
        if "'" + tag + "'" in problem_tags:
            count += 1

    return count == len(tags)


def convert_submissions_to_string(problems, number):
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
            submissions += f"(1 day ago)\n"
        else:
            submissions += f"({difference.days} days ago)\n"

        if count == number:
            break

        count += 1

    return submissions, count