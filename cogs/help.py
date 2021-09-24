import discord
from discord.ext import commands


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
            Embed = discord.Embed(title="Help Menu",
                                  description="Type `-help command` to learn about a specific command.",
                                  color=0xff0000)

            Embed.add_field(
                name="user", value="Displays information about a user.", inline=False)
            Embed.add_field(
                name="stalk", value="Displays the last n problems solved by a user.", inline=False)
            Embed.add_field(
                name="problem", value="Displays a random problem.", inline=False)
            Embed.add_field(
                name="upcoming", value="Displays the list of upcoming Codeforces contests.", inline=False)
            Embed.add_field(
                name="duel", value="Challenges another user to a duel over a problem.", inline=False)
            Embed.add_field(
                name="lockout", value="Challenges another user to a lockout match.", inline=False)
            Embed.add_field(
                name="plotrating", value="Plots the problems done by a user, grouped by rating.", inline=False)
            Embed.add_field(
                name="plotindex", value="Plots the problems done by a user, grouped by contest index.", inline=False)
            Embed.add_field(
                name="plottags", value="Plots the problems done by a user, grouped by tags.", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "user":
            Embed = discord.Embed(title="user",
                                  description="Displays information about a user.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-user <codeforces_handle>`", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "stalk":
            Embed = discord.Embed(title="stalk",
                                  description="Displays the last n problems solved by a user (10 by default).",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-stalk <codeforces_handle>` - Displays last 10 submissions of the user\n`-stalk <codeforces_handle> <n>` - Displays last n submissions of the user")

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "problem":
            Embed = discord.Embed(title="problem",
                                  description="Displays a random problem of optional rating and/or tags.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-problem` - Displays a random problem.\n`-problem <rating>` - Displays a random problem of that rating.\n`-problem <list_of_tags>` - Displays a random problem of those tags (multiple tags are allowed).\n`-problem <rating> <list_of_tags>` - Displays a random problem of those tags and rating (order does not matter).\n\nNote: For tags like \"binary search\", enclose the tag in double quotes.", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "upcoming":
            Embed = discord.Embed(title="upcoming",
                                  description="Displays information about upcoming contests.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-upcoming`", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "duel":
            Embed = discord.Embed(title="duel",
                                  description="Challenges another user to a duel over a problem.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-duel @<discord_user> <optional_rating> <optional_tags>` - To challenge a user\n`-endduel` - To end a duel and decide the result (only if a duel is in progress).", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "plotrating":
            Embed = discord.Embed(title="plotrating",
                                  description="Plots the problems done by a user, grouped by rating.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-plotrating <codeforces_handle>`", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "plotindex":
            Embed = discord.Embed(title="plotindex",
                                  description="Plots the problems done by a user, grouped by contest index.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-plotindex <codeforces_handle>`", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "plottags":
            Embed = discord.Embed(title="plottags",
                                  description="Plots the problems done by a user, grouped by tags.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-plottags <codeforces_handle>`", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        elif cmd == "lockout":
            Embed = discord.Embed(title="lockout",
                                  description="Challenges another user to a lockout match.",
                                  color=0xff0000)

            Embed.add_field(
                name="Syntax", value="`-lockout @<discord_user>` - To challenge a user\n", inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url,
                             text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)

        # If an invalid command was given
        else:
            await ctx.send(f":x: Command \"{cmd}\" does not exist!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Help ready!")


def setup(client):
    client.add_cog(Help(client))
