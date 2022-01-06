"""
The Stalk class, containing all the commands related to history of problems solved by users.
"""


from discord.ext import commands
import logging

from botforces.utils.constants import NUMBER_OF_ACS
from botforces.utils.api import get_user_submissions
from botforces.utils.discord_common import create_submissions_embed
from botforces.utils.services import convert_submissions_to_string


class Stalk(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stalk(self, ctx, handle=None, number=NUMBER_OF_ACS):
        """
        Command to display the last n ACs of a user.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        if handle is None:
            await ctx.send(":x: Please provide a handle.")
            return

        # Displaying the "Typing..." message while the data is being fetched
        async with ctx.typing():
            problems = await get_user_submissions(ctx, handle)

            if not problems:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            # Filtering solved submissions
            problems = list(
                filter(lambda problem: problem["verdict"] == "OK", problems)
            )
            submissions, count = await convert_submissions_to_string(problems, number)

            # Checking if user has made any submissions
            if submissions == "":
                await ctx.send(f"{handle} has not solved any problems!")
                return

            # Creating an embed
            Embed = await create_submissions_embed(
                submissions, count, handle, ctx.author
            )

        # Sending the embed
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("-Stalk ready!")


def setup(client):
    client.add_cog(Stalk(client))
