import discord
import aiohttp
from discord.ext import commands


class Stalk(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ERROR HANDLING TO BE DONE - ALL ACS ONLY + PROBLEMS WITH NO RATINGS
    # Command to display the last n submissions of a user
    @ commands.command()
    async def stalk(self, ctx, handle, number=10):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://codeforces.com/api/user.status?handle={}&count={}'.format(handle, number)) as r:

                # If user was not found
                if not r.ok:
                    await ctx.send("Sorry, user with handle {} could not be found.".format(handle))
                    return

                # Reading the data as JSON data and storing the dictionary in data variable
                data = await r.json()

                # Creating the string of submissions to be the description of Embed
                submissions = ''
                count = 1
                for problem in data["result"]:
                    if count == number:
                        submissions += "{}. {} - {} ({})".format(
                            count, problem["problem"]["name"], problem["problem"]["rating"], problem["verdict"])
                    else:
                        submissions += "{}. {} - {} ({})\n".format(
                            count, problem["problem"]["name"], problem["problem"]["rating"], problem["verdict"])
                    count += 1

                # Creating an embed
                Embed = discord.Embed(
                    title="Last {} submissions of {}".format(number, handle),
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
