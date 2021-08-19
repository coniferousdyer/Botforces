import discord
import aiohttp
import datetime
import time
import csv
from discord.ext import commands


class Upcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display upcoming contests
    @commands.command()
    async def upcoming(self, ctx):
        async with aiohttp.ClientSession() as session:

            with open("data/contests.csv") as csvFile:
                contestList = list(csv.reader(csvFile))

            # Reversing the contest list
            contestList.reverse()

            # Creating embed
            Embed = discord.Embed(title="List of upcoming contests",
                                  color=0xff0000)

            # Adding each contest as a field to the embed
            for contest in contestList:

                # Converting times to int from str
                contest[2] = int(contest[2])
                contest[3] = int(contest[3])

                # Obtaining the time of the contest (dateList[0] -> date, dateList[1] -> time)
                date = str(datetime.datetime.fromtimestamp(
                    contest[3]))
                dateList = date.split()
                dateList[0] = dateList[0].split("-")
                dateList[1] = dateList[1].split(":")

                date = datetime.datetime(int(dateList[0][0]), int(dateList[0][1]), int(
                    dateList[0][2]), int(dateList[1][0]), int(dateList[1][1]), int(dateList[1][2]))
                dateString = date.strftime("%b %d, %Y, %H:%M")

                # Obtaining contest duration
                duration = str(datetime.timedelta(
                    seconds=contest[2]))
                duration = duration.split(":")

                Embed.add_field(
                    name=contest[1], value=f"{contest[0]} - {dateString} {time.tzname[0]} - {duration[0]} hrs, {duration[1]} mins", inline=False)

                Embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=str(ctx.author))

            # Sending embed
            await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Upcoming ready!")


def setup(client):
    client.add_cog(Upcoming(client))
