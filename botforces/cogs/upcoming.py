"""
The Upcoming class, containing the commands related to upcoming contests.
"""


import logging
from discord.ext import commands

from botforces.utils.db import get_contests_from_db
from botforces.utils.discord_common import create_contest_embed


class Upcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def upcoming(self, ctx):
        """
        Command to display upcoming contests.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Obtains the upcoming contests from the database
        contestList = (await get_contests_from_db())[::-1]

        # Creating embed
        Embed = await create_contest_embed(contestList, ctx.author)

        # Sending embed
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("-Upcoming ready!")


def setup(client):
    client.add_cog(Upcoming(client))
