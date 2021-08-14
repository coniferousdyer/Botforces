import discord
import aiohttp
import datetime
import time
from discord.ext import commands


class Upcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to display upcoming contests
    @commands.command()
    async def upcoming(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://codeforces.com/api/contest.list') as r:

                # If URL was not found
                if not r.ok:
                    await ctx.send("Sorry, an error occurred.")
                    return

                # Reading the data as JSON data and storing the dictionary in data variable
                data = await r.json()

                # Creating a list to store upcoming contests
                contestList = []
                for contest in data["result"]:
                    if contest["phase"] != "BEFORE":
                        break
                    contestList.append(contest)

                # Reversing the contest list
                contestList.reverse()

                # Creating embed
                Embed = discord.Embed(title="List of upcoming contests",
                                      color=0xff0000)

                # Adding each contest as a field to the embed
                for contest in contestList:

                    # Obtaining the time of the contest (dateList[0] -> date, dateList[1] -> time)
                    date = str(datetime.datetime.fromtimestamp(
                        contest["startTimeSeconds"]))
                    dateList = date.split()
                    dateList[0] = dateList[0].split("-")
                    dateList[1] = dateList[1].split(":")

                    date = datetime.datetime(int(dateList[0][0]), int(dateList[0][1]), int(
                        dateList[0][2]), int(dateList[1][0]), int(dateList[1][1]), int(dateList[1][2]))
                    dateString = date.strftime("%b %d, %Y, %H:%M")

                    # Obtaining contest duration
                    duration = str(datetime.timedelta(
                        seconds=contest["durationSeconds"]))
                    duration = duration.split(":")

                    Embed.add_field(name=contest["name"], value="{} - {} {} - {} hrs, {} mins".format(
                        contest["id"], dateString, time.tzname[0], duration[0], duration[1]), inline=False)

                    Embed.set_footer(icon_url=ctx.author.avatar_url,
                                     text=str(ctx.author))

                # Sending embed
                await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Upcoming ready!")


def setup(client):
    client.add_cog(Upcoming(client))
