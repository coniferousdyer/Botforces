"""
The Plot class, containing the commands related to plotting of problem statistics.
"""


import logging
import os
from discord.ext import commands
from collections import defaultdict

from botforces.utils.api import get_user_submissions
from botforces.utils.services import sort_dict_by_value
from botforces.utils.graph import (
    plot_rating_bar_chart,
    plot_index_bar_chart,
    plot_tags_bar_chart,
)
from botforces.utils.discord_common import (
    create_rating_plot_embed,
    create_index_plot_embed,
    create_tags_plot_embed,
)


class Plot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def plotrating(self, ctx, handle=None):
        """
        Displays the plot of number of problems solved by a user according to rating.
        """

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        if handle is None:
            await ctx.send(":x: Please provide a handle.")
            return

        async with ctx.typing():
            problemList = await get_user_submissions(ctx, handle)

            if problemList is None:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            problemList = list(
                filter(lambda problem: problem["verdict"] == "OK", problemList)
            )

            resDict = defaultdict(int)
            unique_map = {}

            for problem in problemList:
                if "rating" in problem["problem"]:
                    # Ensuring that the problem is not a duplicate
                    if problem["problem"]["name"] not in unique_map:
                        unique_map[problem["problem"]["name"]] = True
                        rating = problem["problem"]["rating"]
                        resDict[str(rating)] += 1

            if not resDict:
                await ctx.send(f"{handle} has not solved any problems!")
                return

            resDict = await sort_dict_by_value(resDict)
            File = await plot_rating_bar_chart(resDict)
            Embed = await create_rating_plot_embed(handle, ctx.author)

        # Sending embed
        await ctx.send(file=File, embed=Embed)
        os.remove("figure.png")

    @commands.command()
    async def plotindex(self, ctx, handle=None):
        """
        Displays the plot of number of problems solved by a user according to index.
        """

        if handle is None:
            await ctx.send(":x: Please provide a handle.")
            return

        async with ctx.typing():
            problemList = await get_user_submissions(ctx, handle)

            if problemList is None:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            problemList = list(
                filter(lambda problem: problem["verdict"] == "OK", problemList)
            )

            resDict = defaultdict(int)
            unique_map = {}

            for problem in problemList:
                if "index" in problem["problem"]:
                    # Ensuring that the problem is not a duplicate
                    if problem["problem"]["name"] not in unique_map:
                        unique_map[problem["problem"]["name"]] = True
                        index = problem["problem"]["index"][0]
                        resDict[index] += 1

            if not resDict:
                await ctx.send(f"{handle} has not solved any problems!")
                return

            resDict = await sort_dict_by_value(resDict)
            File = await plot_index_bar_chart(resDict)
            Embed = await create_index_plot_embed(handle, ctx.author)

        # Sending embed
        await ctx.send(file=File, embed=Embed)
        os.remove("figure.png")

    @commands.command()
    async def plottags(self, ctx, handle=None):
        """
        Displays the plot of number of problems solved by a user according to tags.
        """

        if handle is None:
            await ctx.send(":x: Please provide a handle.")
            return

        async with ctx.typing():
            problemList = await get_user_submissions(ctx, handle)

            if problemList is None:
                await ctx.send(
                    f":x: Sorry, user with handle {handle} could not be found."
                )
                return

            problemList = list(
                filter(lambda problem: problem["verdict"] == "OK", problemList)
            )

            resDict = defaultdict(int)
            unique_map = {}

            for problem in problemList:
                if "tags" in problem["problem"]:
                    # Ensuring that the problem is not a duplicate
                    if problem["problem"]["name"] not in unique_map:
                        unique_map[problem["problem"]["name"]] = True
                        tags = problem["problem"]["tags"]
                        for tag in tags:
                            resDict[tag] += 1

            if not resDict:
                await ctx.send(f"{handle} has not solved any problems!")
                return

            resDict = await sort_dict_by_value(resDict)
            File = await plot_tags_bar_chart(resDict)
            Embed = await create_tags_plot_embed(handle, ctx.author)

        # Sending embed
        await ctx.send(file=File, embed=Embed)
        os.remove("figure.png")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("-Plot ready!")


def setup(client):
    client.add_cog(Plot(client))
