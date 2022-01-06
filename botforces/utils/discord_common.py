"""
Contains functions related to Discord-specific features, such as embeds.
"""


import discord
import datetime
import time

from botforces.utils.constants import (
    NUMBER_OF_ACS,
    USER_WEBSITE_URL,
    PROBLEM_WEBSITE_URL,
)
from botforces.utils.services import enclose_tags_in_spoilers


"""
User embeds.
"""


async def create_user_embed(user, author, color):
    """
    Creates an embed with user information.
    """

    Embed = discord.Embed(
        title=user["handle"],
        url=f"{USER_WEBSITE_URL}{user['handle']}",
        color=color,
    )

    Embed.set_thumbnail(url=user["avatar"])

    if "firstName" in user and "lastName" in user:
        Embed.add_field(
            name="Name",
            value=f"{user['firstName']} {user['lastName']}",
            inline=False,
        )

    if "city" in user and "country" in user:
        Embed.add_field(
            name="City",
            value=f"{user['city']}, {user['country']}",
            inline=False,
        )

    if "rank" in user:
        Embed.add_field(
            name="Rank",
            value=user["rank"].title(),
            inline=False,
        )
    else:
        Embed.add_field(name="Rank", value="Unranked", inline=False)

    if "rating" in user:
        Embed.add_field(
            name="Rating",
            value=user["rating"],
            inline=False,
        )

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Problem embeds.
"""


async def create_problem_embed(problem, author):
    """
    Creates an embed with problem information.
    """

    Embed = discord.Embed(
        title=f"{problem['contestId']}{problem['contestIndex']}. {problem['name']}",
        url=f"{PROBLEM_WEBSITE_URL}{problem['contestId']}/{problem['contestIndex']}",
        color=0xFF0000,
    )

    Embed.add_field(name="Rating", value=problem[4], inline=False)

    # Printing the tags in spoilers
    if problem["tags"] != "[]":
        tags = await enclose_tags_in_spoilers(problem["tags"])
        Embed.add_field(name="Tags", value=tags)

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Upcoming contests embeds.
"""


async def create_contest_embed(contestList, author):
    """
    Creates an embed with contest information.
    """

    Embed = discord.Embed(title="List of upcoming contests", color=0xFF0000)

    # Adding each contest as a field to the embed
    for contest in contestList:

        # Obtaining the start time of the contest
        date = datetime.datetime.fromtimestamp(contest["startTimeSeconds"])
        dateString = date.strftime("%b %d, %Y, %H:%M")

        # Obtaining contest duration
        duration = datetime.timedelta(seconds=contest["durationSeconds"])
        hours = duration.seconds // 3600
        minutes = (duration.seconds // 60) % 60

        Embed.add_field(
            name=contest["name"],
            value=f"{contest['id']} - {dateString} {time.tzname[0]} - {hours} hrs, {minutes} mins",
            inline=False,
        )

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Stalk embeds.
"""


async def create_submissions_embed(submissions, count, handle, author):
    """
    Creates an embed with information about a user's last n solved problems.
    """

    Embed = discord.Embed(
        title=f"Last {count} solved by {handle}",
        description=submissions,
        color=0xFF0000,
    )

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Graph embeds.
"""


async def create_rating_plot_embed(handle, author):
    """
    Creates an embed with the rating plot of a user.
    """

    Embed = discord.Embed(
        title=f"{handle}'s solved problems",
        description="Note: ? refers to problems that do not have a rating on Codeforces.",
        color=0xFF0000,
    )
    Embed.set_image(url="attachment://figure.png")
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_index_plot_embed(handle, author):
    """
    Creates an embed with the index plot of a user.
    """

    Embed = discord.Embed(title=f"{handle}'s solved problems", color=0xFF0000)
    Embed.set_image(url="attachment://figure.png")
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_tags_plot_embed(handle, author):
    """
    Creates an embed with the tags plot of a user.
    """

    Embed = discord.Embed(title=f"{handle}'s solved problems", color=0xFF0000)
    Embed.set_image(url="attachment://figure.png")
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Help embeds.
"""


async def create_general_help_embed(author):
    """
    Displays an embed with instructions on how to use all commands.
    """

    Embed = discord.Embed(
        title="Help Menu",
        description="Type `-help command` to learn about a specific command.",
        color=0xFF0000,
    )

    Embed.add_field(
        name="user", value="Displays information about a user.", inline=False
    )
    Embed.add_field(
        name="stalk",
        value="Displays the last n problems solved by a user.",
        inline=False,
    )
    Embed.add_field(name="problem", value="Displays a random problem.", inline=False)
    Embed.add_field(
        name="upcoming",
        value="Displays the list of upcoming Codeforces contests.",
        inline=False,
    )
    Embed.add_field(
        name="duel",
        value="Challenges another user to a duel over a problem.",
        inline=False,
    )
    Embed.add_field(
        name="plotrating",
        value="Plots the problems done by a user, grouped by rating.",
        inline=False,
    )
    Embed.add_field(
        name="plotindex",
        value="Plots the problems done by a user, grouped by contest index.",
        inline=False,
    )
    Embed.add_field(
        name="plottags",
        value="Plots the problems done by a user, grouped by tags.",
        inline=False,
    )

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_user_help_embed(author):
    """
    Displays an embed with instructions on how to use the user command.
    """

    Embed = discord.Embed(
        title="user", description="Displays information about a user.", color=0xFF0000
    )
    Embed.add_field(name="Syntax", value="`-user <codeforces_handle>`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_stalk_help_embed(author):
    """
    Displays an embed with instructions on how to use the stalk command.
    """

    Embed = discord.Embed(
        title="stalk",
        description=f"Displays the last n problems solved by a user ({NUMBER_OF_ACS} by default).",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax",
        value=f"`-stalk <codeforces_handle>` - Displays last {NUMBER_OF_ACS} submissions of the user\n`-stalk <codeforces_handle> <n>` - Displays last n submissions of the user",
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_problem_help_embed(author):
    """
    Displays an embed with instructions on how to use the problem command.
    """

    Embed = discord.Embed(
        title="problem",
        description="Displays a random problem of optional rating and/or tags.",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax",
        value='`-problem` - Displays a random problem.\n`-problem <rating>` - Displays a random problem of that rating.\n`-problem <list_of_tags>` - Displays a random problem of those tags (multiple tags are allowed).\n`-problem <rating> <list_of_tags>` - Displays a random problem of those tags and rating (order does not matter).\n\nNote: For tags like "binary search", enclose the tag in double quotes.',
        inline=False,
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_upcoming_help_embed(author):
    """
    Displays an embed with instructions on how to use the upcoming command.
    """

    Embed = discord.Embed(
        title="upcoming",
        description="Displays information about upcoming contests.",
        color=0xFF0000,
    )
    Embed.add_field(name="Syntax", value="`-upcoming`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_duel_help_embed(author):
    """
    Displays an embed with instructions on how to use the duel command.
    """

    Embed = discord.Embed(
        title="duel",
        description="Challenges another user to a duel over a problem.",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax",
        value="`-duel @<discord_user> <optional_rating> <optional_tags>` - To challenge a user\n`-endduel` - To end a duel and decide the result (only if a duel is in progress).",
        inline=False,
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_plotrating_help_embed(author):
    """
    Displays an embed with instructions on how to use the plotrating command.
    """

    Embed = discord.Embed(
        title="plotrating",
        description="Plots the problems done by a user, grouped by rating.",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax", value="`-plotrating <codeforces_handle>`", inline=False
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_plotindex_help_embed(author):
    """
    Displays an embed with instructions on how to use the plotindex command.
    """

    Embed = discord.Embed(
        title="plotindex",
        description="Plots the problems done by a user, grouped by contest index.",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax", value="`-plotindex <codeforces_handle>`", inline=False
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


async def create_plottags_help_embed(author):
    """
    Displays an embed with instructions on how to use the plottags command.
    """

    Embed = discord.Embed(
        title="plottags",
        description="Plots the problems done by a user, grouped by tags.",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax", value="`-plottags <codeforces_handle>`", inline=False
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Duel embeds.
"""


async def create_duel_begin_embed(problem, author, opponent):
    """
    Displays an embed with information about the duel.
    """

    Embed = discord.Embed(
        title=f"{problem['contestId']}{problem['contestIndex']}. {problem['name']}",
        url=f"{PROBLEM_WEBSITE_URL}{problem['contestId']}/{problem['contestIndex']}",
        description="The duel starts now!",
        color=0xFF0000,
    )

    Embed.add_field(name="Rating", value=problem["rating"], inline=False)

    # Printing the tags in spoilers
    if problem["tags"] != "[]":
        tags = await enclose_tags_in_spoilers(problem["tags"])
        Embed.add_field(name="Tags", value=tags)

    Embed.add_field(
        name="Duel",
        value=f"{author.display_name} vs {opponent.display_name}",
        inline=False,
    )

    return Embed


async def create_duels_embed(duels):
    """
    Displays an embed with information about all ongoing duels.
    """

    Embed = discord.Embed(
        title="Ongoing duels",
        color=0xFF0000,
    )

    # Adding fields to embed
    for duel in duels:
        date = datetime.datetime.strptime(
            duel["startTime"], "%Y-%m-%d %H:%M:%S.%f"
        ).strftime("%b %d, %Y %H:%M:%S")
        Embed.add_field(
            name=f"{duel['handle_1']} vs {duel['handle_2']}",
            value=f"Problem: {PROBLEM_WEBSITE_URL}{duel['contestId']}/{duel['contestIndex']}\nStart Time: {date} {time.tzname[0]}",
            inline=False,
        )

    return Embed
