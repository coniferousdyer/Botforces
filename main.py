"""
The main module; the entry point of the bot.
"""


import discord
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from discord_sentry_reporting import use_sentry

from botforces.utils.api import get_all_problems, get_all_upcoming_contests
from botforces.utils.db import (
    create_users_table,
    create_contests_table,
    create_duels_table,
    create_problems_table,
    store_contest,
    store_problem,
)

load_dotenv()

client = commands.Bot(command_prefix=os.getenv("BOT_PREFIX"), help_command=None)

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

    # Creating a directory to store logs
    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    # Setting up the logger
    logging.basicConfig(
        handlers=[
            RotatingFileHandler("./logs/botforces.log", maxBytes=100000, backupCount=10)
        ],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Setting up Sentry
    use_sentry(client, dsn=os.getenv("SENTRY_DSN"))

    # Setting the bot activity on Discord
    await client.change_presence(activity=discord.Game(name="Codeforces"))
    update_db.start()
    await create_users_table()
    await create_duels_table()

    logging.info("Bot is online!")


@tasks.loop(hours=1)
async def update_db():
    """
    Updates the database periodically (per hour).
    """

    await create_contests_table()
    await create_problems_table()

    # Obtaining the list of all upcoming contests
    contests = await get_all_upcoming_contests()

    # Storing the contests in the database
    for contest in contests:
        if contest["phase"] == "BEFORE":
            await store_contest(contest)
        else:
            break

    logging.info("Updated contests.")

    # Obtaining the list of all rated problems
    problems = await get_all_problems()

    # Storing the problems in the database
    for problem in problems:
        await store_problem(problem)

    logging.info("Updated problems.")


client.run(os.getenv("DISCORD_TOKEN"))
