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
            async with session.get(f'https://codeforces.com/api/user.status?handle={handle}&count={number}') as r:

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
                    if count == number:
                        submissions += f"{count}. {problem['problem']['name']} - {problem['problem']['rating']} ({problem['verdict']})"
                    else:
                        submissions += f"{count}. {problem['problem']['name']} - {problem['problem']['rating']} ({problem['verdict']})\n"
                    count += 1

                # Creating an embed
                Embed = discord.Embed(
                    title=f"Last {number} submissions of {handle}",
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
