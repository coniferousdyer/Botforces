"""
The Problem class, containing all the commands related to problem suggestion.
"""


import random
import logging
from discord.ext import commands

from botforces.utils.db import get_problems_from_db
from botforces.utils.discord_common import create_problem_embed
from botforces.utils.services import separate_rating_and_tags


class Problem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def problem(self, ctx, *args):
        """
        Command to suggest a random problem, with optional tags and rating.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Obtaining the problems from the database
        rating, tags = await separate_rating_and_tags(args)
        problemList = await get_problems_from_db(rating, tags)

        # In case no problems are found
        if len(problemList) == 0:
            await ctx.send(":x: Sorry, no problems could be found. Please try again.")
            return

        # Storing a random problem
        problem = problemList[random.randint(0, len(problemList) - 1)]

        # Creating an embed
        Embed = await create_problem_embed(problem, ctx.author)

        # Sending embed
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("-Problem ready!")


def setup(client):
    client.add_cog(Problem(client))
