from discord.ext import commands

from botforces.utils.api import get_user_by_handle
from botforces.utils.discord_common import create_user_embed
from botforces.utils.services import map_rank_to_color


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to search for a user and display their basic details
    @commands.command()
    async def user(self, ctx, handle):
        """
        Searches for a user and displays their basic details.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
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

    @commands.Cog.listener()
    async def on_ready(self):
        print("-User ready!")


def setup(client):
    client.add_cog(User(client))
