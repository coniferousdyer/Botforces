import discord
import aiohttp
import os
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np


class Plot(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display the plot of problems solved by a user according to rating
    @commands.command()
    async def plotrating(self, ctx, handle):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://codeforces.com/api/user.status?handle={handle}') as r:

                # If the user was not found
                if not r.ok:
                    await ctx.send(f"Sorry, user with handle {handle} could not be found.")
                    return

                # Reading the data as JSON data and storing the dictionary in data variable
                data = await r.json()
                problemList = data["result"]

                # Checking submissions
                pDict = dict({})

                for problem in problemList:
                    if problem["verdict"] == "OK":
                        if "rating" in problem["problem"]:
                            pDict[problem["problem"]["name"]
                                  ] = problem["problem"]["rating"]
                        else:
                            pDict[problem["problem"]["name"]] = "0"

                resDict = dict({})

                for rating in pDict.values():
                    resDict[rating] = resDict.get(rating, 0) + 1

                resDict = dict(sorted(resDict.items(), key=lambda x: x[1]))

                # Plotting graph
                x = np.array(list(resDict.keys()))
                y = np.array(list(resDict.values()))

                plt.clf()
                plt.bar(x, y)
                plt.xticks(fontsize=7, rotation=45)
                plt.xlabel("Rating", fontsize=7)
                plt.ylabel("Number", fontsize=7)

                for i in range(len(y)):
                    plt.annotate(str(y[i]), xy=(x[i], y[i]),
                                 ha='center', va='bottom').set_fontsize(7)

                # Saving file temporarily
                plt.savefig("figure.png")
                File = discord.File("figure.png")

                # Creating an embed
                Embed = discord.Embed(
                    title=f"{handle}'s solved problems",
                    description="Note: Rating 0 refers to problems that do not have a rating on Codeforces.",
                    color=0xff0000)
                Embed.set_image(url="attachment://figure.png")

                Embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=str(ctx.author))

                # Sending embed
                await ctx.send(file=File, embed=Embed)

                # Deleting temporary file
                os.remove("figure.png")

    # Command to display the plot of problems solved by a user according to index
    @commands.command()
    async def plotindex(self, ctx, handle):
        pass

    # Command to display the plot of problems solved by a user according to tags
    @commands.command()
    async def plottags(self, ctx, handle):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Plot ready!")


def setup(client):
    client.add_cog(Plot(client))
