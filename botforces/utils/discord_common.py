import discord
import datetime
import time

from botforces.utils.constants import USER_WEBSITE_URL, PROBLEM_WEBSITE_URL


"""
User embeds.
"""


def create_user_embed(user, author, color):
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


def create_problem_embed(problem, author):
    """
    Creates an embed with problem information.
    """

    Embed = discord.Embed(
        title=f"{problem[0]}{problem[1]}. {problem[2]}",
        url=f"{PROBLEM_WEBSITE_URL}{problem[0]}/{problem[1]}",
        color=0xFF0000,
    )

    Embed.add_field(name="Rating", value=problem[4], inline=False)

    # Printing the tags in spoilers
    if problem[3] != "[]":
        tags = problem[3].split(", ")
        tags = [tag.strip("[]'") for tag in tags]
        tags = map(lambda str: "||" + str + "||", tags)
        tags = ",".join(tags)
        Embed.add_field(name="Tags", value=tags)

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Upcoming contests embeds.
"""


def create_contest_embed(contestList, author):
    """
    Creates an embed with contest information.
    """

    Embed = discord.Embed(title="List of upcoming contests", color=0xFF0000)

    # Adding each contest as a field to the embed
    for contest in contestList:

        # Obtaining the time of the contest (dateList[0] -> date, dateList[1] -> time)
        date = str(datetime.datetime.fromtimestamp(contest[3]))
        dateList = date.split()
        dateList[0] = dateList[0].split("-")
        dateList[1] = dateList[1].split(":")

        # dateList[i][0] -> year/hour
        # dateList[i][1] -> month/minute
        # dateList[i][2] -> day/second
        date = datetime.datetime(
            int(dateList[0][0]),
            int(dateList[0][1]),
            int(dateList[0][2]),
            int(dateList[1][0]),
            int(dateList[1][1]),
            int(dateList[1][2]),
        )
        dateString = date.strftime("%b %d, %Y, %H:%M")

        # Obtaining contest duration
        duration = str(datetime.timedelta(seconds=contest[2]))
        duration = duration.split(":")

        Embed.add_field(
            name=contest[1],
            value=f"{contest[0]} - {dateString} {time.tzname[0]} - {duration[0]} hrs, {duration[1]} mins",
            inline=False,
        )

    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


"""
Stalk embeds.
"""


def create_submissions_embed(submissions, count, handle, author):
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


def create_rating_plot_embed(handle, author):
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


def create_index_plot_embed(handle, author):
    """
    Creates an embed with the index plot of a user.
    """

    Embed = discord.Embed(title=f"{handle}'s solved problems", color=0xFF0000)
    Embed.set_image(url="attachment://figure.png")
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


def create_tags_plot_embed(handle, author):
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


def create_general_help_embed(author):
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
        name="lockout",
        value="Challenges another user to a lockout match.",
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


def create_user_help_embed(author):
    """
    Displays an embed with instructions on how to use the user command.
    """

    Embed = discord.Embed(
        title="user", description="Displays information about a user.", color=0xFF0000
    )
    Embed.add_field(name="Syntax", value="`-user <codeforces_handle>`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


def create_stalk_help_embed(author):
    """
    Displays an embed with instructions on how to use the stalk command.
    """

    Embed = discord.Embed(
        title="stalk",
        description="Displays the last n problems solved by a user (10 by default).",
        color=0xFF0000,
    )
    Embed.add_field(
        name="Syntax",
        value="`-stalk <codeforces_handle>` - Displays last 10 submissions of the user\n`-stalk <codeforces_handle> <n>` - Displays last n submissions of the user",
    )
    Embed.set_footer(icon_url=author.avatar_url, text=str(author))

    return Embed


def create_problem_help_embed(author):
    Embed = discord.Embed(title="problem",
                            description="Displays a random problem of optional rating and/or tags.",
                            color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-problem` - Displays a random problem.\n`-problem <rating>` - Displays a random problem of that rating.\n`-problem <list_of_tags>` - Displays a random problem of those tags (multiple tags are allowed).\n`-problem <rating> <list_of_tags>` - Displays a random problem of those tags and rating (order does not matter).\n\nNote: For tags like \"binary search\", enclose the tag in double quotes.", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))


    return Embed


def create_upcoming_help_embed(author):
    Embed = discord.Embed(title="upcoming",
                                  description="Displays information about upcoming contests.",
                                  color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-upcoming`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))


    return Embed


def create_duel_help_embed(author):
    Embed = discord.Embed(title="duel",
                                  description="Challenges another user to a duel over a problem.",
                                  color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-duel @<discord_user> <optional_rating> <optional_tags>` - To challenge a user\n`-endduel` - To end a duel and decide the result (only if a duel is in progress).", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))

    return Embed


def create_plotrating_help_embed(author):
    Embed = discord.Embed(title="plotrating",
                            description="Plots the problems done by a user, grouped by rating.",
                            color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-plotrating <codeforces_handle>`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))

    return Embed


def create_plotindex_help_embed(author):
    Embed = discord.Embed(title="plotindex",
                                  description="Plots the problems done by a user, grouped by contest index.",
                                  color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-plotindex <codeforces_handle>`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))
    
    return Embed


def create_plottags_help_embed(author):
    Embed = discord.Embed(title="plottags",
                                  description="Plots the problems done by a user, grouped by tags.",
                                  color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-plottags <codeforces_handle>`", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))

    return Embed


def create_lockout_help_embed(author):
    Embed = discord.Embed(title="lockout",
                            description="Challenges another user to a lockout match.",
                            color=0xff0000)
    Embed.add_field(
        name="Syntax", value="`-lockout @<discord_user>` - To challenge a user\n", inline=False)
    Embed.set_footer(icon_url=author.avatar_url,
                        text=str(author))

    return Embed