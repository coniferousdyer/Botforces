import discord
import aiohttp
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to search for a user and display their basic details
    @commands.command()
    async def user(self, ctx, handle):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://codeforces.com/api/user.info?handles={}'.format(handle)) as r:

                # If the user was not found
                if not r.ok:
                    await ctx.send("Sorry, user with handle {} could not be found.".format(handle))
                    return

                # Reading the data as JSON data and storing the dictionary in data variable
                data = await r.json()

                # Assigning a color according to rank
                color = 0xff0000
                if data["result"][0]["rank"] == "newbie":
                    color = 0x918f8e
                elif data["result"][0]["rank"] == "pupil":
                    color = 0x087515
                elif data["result"][0]["rank"] == "specialist":
                    color = 0x1af2f2
                elif data["result"][0]["rank"] == "expert":
                    color = 0x1300f9
                elif data["result"][0]["rank"] == "candidate master":
                    color = 0xb936ee
                elif data["result"][0]["rank"] == "master" or data["result"][0]["rank"] == "international master":
                    color = 0xeebb36

                # Creating an embed
                Embed = discord.Embed(title=data["result"][0]["handle"],
                                      url="https://codeforces.com/profile/{}".format(
                                          data["result"][0]["handle"]),
                                      color=color)

                Embed.set_thumbnail(url=data["result"][0]["avatar"])

                if 'firstName' in data["result"][0] and 'lastName' in data["result"][0]:
                    Embed.add_field(
                        name="Name", value=data["result"][0]["firstName"] + ' ' + data["result"][0]["lastName"], inline=False)

                if 'city' in data["result"][0] and 'country' in data["result"][0]:
                    Embed.add_field(
                        name="City", value=data["result"][0]["city"] + ', ' + data["result"][0]["country"], inline=False)

                Embed.add_field(
                    name="Rank", value=data["result"][0]["rank"].title(), inline=False)
                Embed.add_field(name="Rating",
                                value=data["result"][0]["rating"], inline=False)

                Embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=str(ctx.author))

                # Sending the embed
                await ctx.send(embed=Embed)


def setup(client):
    client.add_cog(User(client))
