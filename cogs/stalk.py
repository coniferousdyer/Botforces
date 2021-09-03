import discord
import aiohttp
import datetime
from discord.ext import commands


class Stalk(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display the last n ACs of a user
    @ commands.command()
    async def stalk(self, ctx, handle=None, number=10):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        if handle == None:
            await ctx.send(":x: Please provide a handle.")
            return

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://codeforces.com/api/user.status?handle={handle}') as r:

                    # If user was not found
                    if not r.ok:
                        await ctx.send(f":x: Sorry, user with handle {handle} could not be found.")
                        return

                    # Reading the data as JSON data and storing the dictionary in data variable
                    data = await r.json()

                    # Getting the time that the request was made at
                    startTime = datetime.datetime.now()

                    # Creating the string of submissions to be the description of Embed
                    submissions = ''
                    count = 1
                    for problem in data["result"]:
                        if problem['verdict'] == "OK":
                            if 'rating' in problem['problem']:
                                if count == number:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - {problem['problem']['rating']} "
                                    difference = startTime - \
                                        datetime.datetime.fromtimestamp(int(problem["creationTimeSeconds"]))
                                    if difference.days == 1:
                                        submissions += f"(1 day ago)"
                                    else:
                                        submissions += f"({difference.days} days ago)"
                                    break
                                else:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - {problem['problem']['rating']} "
                                    difference = startTime - \
                                        datetime.datetime.fromtimestamp(int(problem["creationTimeSeconds"]))
                                    if difference.days == 1:
                                        submissions += f"(1 day ago)\n"
                                    else:
                                        submissions += f"({difference.days} days ago)\n"
                                count += 1
                            else:
                                if count == number:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - ? "
                                    difference = startTime - \
                                        datetime.datetime.fromtimestamp(int(problem["creationTimeSeconds"]))
                                    if difference.days == 1:
                                        submissions += f"(1 day ago)"
                                    else:
                                        submissions += f"({difference.days} days ago)"
                                    break
                                else:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - ? "
                                    difference = startTime - \
                                        datetime.datetime.fromtimestamp(int(problem["creationTimeSeconds"]))
                                    if difference.days == 1:
                                        submissions += f"(1 day ago)\n"
                                    else:
                                        submissions += f"({difference.days} days ago)\n"
                                count += 1

                    # Checking if user has made any submissions
                    if submissions == '':
                        await ctx.send(f"{handle} has not solved any problems!")
                        return

                    # Creating an embed
                    Embed = discord.Embed(
                        title=f"Last {count} solved by {handle}",
                        description=submissions,
                        color=0xff0000)

                    Embed.set_footer(icon_url=ctx.author.avatar_url,
                                     text=str(ctx.author))

        # Sending the embed
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Stalk ready!")


def setup(client):
    client.add_cog(Stalk(client))
