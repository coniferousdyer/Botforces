import discord
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv

from botforces.utils.api import get_all_problems, get_all_upcoming_contests
from botforces.utils.db import (
    create_contests_table,
    create_duels_table,
    create_problems_table,
    store_contest,
    store_problem,
)


client = commands.Bot(command_prefix="-", help_command=None)

load_dotenv()

# Loading cogs
for filename in os.listdir("botforces/cogs"):
    if filename.endswith(".py"):
        cog = f"botforces.cogs.{filename[:-3]}"
        try:
            client.load_extension(cog)
        except Exception as exc:
            print(f"Could not load cog {cog}: {str(exc)}")


@client.event
async def on_ready():
    """
    Called when the bot is ready.
    """

    # Setting the bot activity on Discord
    await client.change_presence(activity=discord.Game(name="Codeforces"))
    update_db.start()
    create_duels_table()

    print("Bot is online!")


@tasks.loop(hours=1)
async def update_db():
    """
    Updates the database periodically (per hour).
    """

    create_contests_table()
    create_problems_table()

    # Obtaining the list of all upcoming contests
    contests = await get_all_upcoming_contests()

    # Storing the contests in the database
    for contest in contests:
        if contest["phase"] == "BEFORE":
            store_contest(contest)
        else:
            break

    # Obtaining the list of all rated problems
    problems = await get_all_problems()

    # Storing the problems in the database
    for problem in problems:
        store_problem(problem)


client.run(os.getenv("DISCORD_TOKEN"))
