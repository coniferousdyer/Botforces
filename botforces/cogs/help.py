from discord.ext import commands

from botforces.utils.discord_common import (
    create_general_help_embed,
    create_stalk_help_embed,
    create_user_help_embed,
    create_problem_help_embed,
    create_upcoming_help_embed,
    create_duel_help_embed,
    create_plotrating_help_embed,
    create_plotindex_help_embed,
    create_plottags_help_embed,
)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display all commands (and optionally, descriptions of what they do)
    @commands.command()
    async def help(self, ctx, cmd=None):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # If no parameter was provided
        if cmd == None:
            Embed = await create_general_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "user":
            Embed = await create_user_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "stalk":
            Embed = await create_stalk_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "problem":
            Embed = await create_problem_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "upcoming":
            Embed = await create_upcoming_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "duel" or cmd == "endduel":
            Embed = await create_duel_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plotrating":
            Embed = await create_plotrating_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plotindex":
            Embed = await create_plotindex_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plottags":
            Embed = await create_plottags_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        # If an invalid command was given
        else:
            await ctx.send(f':x: Command "{cmd}" does not exist!')

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Help ready!")


def setup(client):
    client.add_cog(Help(client))
