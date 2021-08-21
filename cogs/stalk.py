import discord
import aiohttp
from discord.ext import commands


class Stalk(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display the last n ACs of a user
    @ commands.command()
    async def stalk(self, ctx, handle=None, number=10):

        if handle == None:
            await ctx.send("Please provide a handle.")
            return

        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://codeforces.com/api/user.status?handle={handle}') as r:

                    # If user was not found
                    if not r.ok:
                        await ctx.send(f"Sorry, user with handle {handle} could not be found.")
                        return

                    # Reading the data as JSON data and storing the dictionary in data variable
                    data = await r.json()

                    # Creating the string of submissions to be the description of Embed
                    submissions = ''
                    count = 1
                    for problem in data["result"]:
                        if problem['verdict'] == "OK":
                            if 'rating' in problem['problem']:
                                if count == number:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - {problem['problem']['rating']}"
                                    break
                                else:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - {problem['problem']['rating']}\n"
                                count += 1
                            else:
                                if count == number:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - ?"
                                    break
                                else:
                                    submissions += f"{count}. [{problem['problem']['name']}](https://codeforces.com/problemset/problem/{problem['problem']['contestId']}/{problem['problem']['index']}) - ?\n"
                                count += 1

                    # Creating an embed
                    Embed = discord.Embed(
                        title=f"Last {number} solved by {handle}",
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
