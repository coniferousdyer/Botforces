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
    create_lockout_help_embed,
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
            Embed = create_general_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "user":
            Embed = create_user_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "stalk":
            Embed = create_stalk_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "problem":
            Embed = create_problem_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "upcoming":
            Embed = create_upcoming_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "duel":
            Embed = create_duel_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plotrating":
            Embed = create_plotrating_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plotindex":
            Embed = create_plotindex_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "plottags":
            Embed = create_plottags_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        elif cmd == "lockout":
            Embed = create_lockout_help_embed(ctx.author)
            await ctx.send(embed=Embed)

        # If an invalid command was given
        else:
            await ctx.send(f':x: Command "{cmd}" does not exist!')

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Help ready!")


def setup(client):
    client.add_cog(Help(client))
