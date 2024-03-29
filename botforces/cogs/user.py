"""
The User class, containing all the commands related to user information.
"""


import logging
from discord.ext import commands

from botforces.utils.api import get_user_by_handle
from botforces.utils.db import store_user, remove_user_from_db
from botforces.utils.discord_common import create_user_embed
from botforces.utils.services import map_rank_to_color


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def user(self, ctx, handle=None):
        """
        Searches for a user and displays their basic details.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Checking if the user provided a handle
        if handle is None:
            await ctx.send(":x: No handle was provided!\n")
            return

        # Displays the "typing..." message while the data is being fetched
        async with ctx.typing():
            user = await get_user_by_handle(ctx, handle)
            if not user:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            # Assigning a color according to rank
            if "rank" in user:
                rank = user["rank"]
            else:
                rank = None

            color = await map_rank_to_color(rank)

            # Creating an embed
            Embed = await create_user_embed(user, ctx.author, color)

        # Sending the embed
        await ctx.send(embed=Embed)

    @commands.command()
    async def register(self, ctx, handle=None):
        """
        Registers a user with the bot.
        Note: A registration is a mapping of the user's Discord ID and Codeforces handle.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Checking if the user provided a handle
        if handle is None:
            await ctx.send(":x: No handle was provided!\n")
            return

        # Displays the "typing..." message while the data is being fetched
        async with ctx.typing():
            user = await get_user_by_handle(ctx, handle)
            if not user:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            # Adding the mapping to the database
            await store_user(ctx.message.author.id, handle)

        # Sending the confirmation message
        await ctx.send(
            f":white_check_mark: Successfully registered {handle} with the bot."
        )

    @commands.command()
    async def unregister(self, ctx):
        """
        Unregisters a user with the bot.
        Note: A registration is a mapping of the user's Discord ID and Codeforces handle.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Displays the "typing..." message while the data is being fetched
        async with ctx.typing():
            # Removing the mapping from the database
            await remove_user_from_db(ctx.message.author.id)

        # Sending the confirmation message
        await ctx.send(":white_check_mark: Successfully unregistered with the bot.")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("-User ready!")


def setup(client):
    client.add_cog(User(client))
