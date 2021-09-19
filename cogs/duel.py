import discord
import aiohttp
import asyncio
import csv
import random
import datetime
from discord.ext import commands


class Duel(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to suggest a random problem, with optional tags and rating
    @commands.command()
    async def duel(self, ctx, usr: discord.User = None, *args):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        async with aiohttp.ClientSession() as session:

            # Checking if a user was mentioned
            if usr == None:
                await ctx.send(":x: Please mention whom you want to duel.")
                return

            if usr.bot or usr == self.client.user:
                await ctx.send(":x: You can't duel a bot.")
                return

            # Checking if the user mentioned themselves
            if usr == ctx.author:
                await ctx.send(":x: You can't duel yourself.")
                return

            reactMsg = await ctx.send(f"<@{usr.id}>, react to this message with :thumbsup: within 30 seconds to accept the duel.")

            # Function to check the reaction on the message
            def check(reaction, user):
                return user == usr and str(reaction.emoji) == '\N{THUMBS UP SIGN}' and reactMsg.id == reaction.message.id

            # Waiting for the reaction
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(":x: Sorry, the duel expired because 30 seconds were up!")
                return
            else:
                await ctx.send(f"<@{usr.id}> has accepted the duel! Send handles of <@{ctx.message.author.id}> and <@{usr.id}> respectively like this within the next 60 seconds:\n```handles <handle of {ctx.author.display_name}> <handle of {usr.display_name}>```")

                def check_2(m):
                    return m.content.startswith("handles") and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author) and len(m.content.split()) == 3
                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check_2)
                except asyncio.TimeoutError:
                    await ctx.send(":x: Sorry, the duel expired because 60 seconds were up!")
                    return
                else:
                    await ctx.send("Starting duel...")
                    handles = msg.content.split()

                # Opening problems.csv and reading the data into a list
                with open('data/problems.csv') as csvFile:
                    problemList = list(csv.reader(csvFile))

                # Initialising rating to 0 and tags to empty list
                rating = 0
                tags = []

                # Separating the rating and the tags
                for arg in args:
                    if arg.isdigit():
                        rating = int(arg)
                    else:
                        tags.append(arg)

                # If rating was given, i.e. rating != 0, then filter the list
                if rating != 0:
                    problemList = list(filter(
                        lambda p: p[4] == f"{rating}", problemList))

                for problem in problemList:
                    problem[3] = problem[3].strip("[]").split(", ")
                    problem[3] = list(map(lambda x: x.strip("'"), problem[3]))

                # If tags were given, i.e. tags is not empty, filter the list
                if tags != []:
                    problemList = list(filter(lambda p: all(
                        x in p[3] for x in tags), problemList))

                # In case no problems are found
                if len(problemList) == 0:
                    await ctx.send(":x: Sorry, no problems could be found. Please try again.")
                    return

                # Storing problem
                problem = problemList[random.randint(0, len(problemList) - 1)]

                # Creating an embed
                Embed = discord.Embed(title=f"{problem[0]}{problem[1]}. {problem[2]}",
                                      url=f"https://codeforces.com/problemset/problem/{problem[0]}/{problem[1]}",
                                      description="The duel starts now!",
                                      color=0xff0000)

                Embed.add_field(
                    name="Rating", value=problem[4], inline=False)

                # Formatting the strings in the list and joining them to form a string
                if tags != [] and problem[3] != []:  
                    problem[3] = map(
                    lambda str: '||' + str + '||', problem[3])  
                    tags = ','.join(problem[3])
                    Embed.add_field(name="Tags", value=tags, inline=False)


                Embed.add_field(
                    name="Duel", value=f"{ctx.author.display_name} vs {usr.display_name}")

                # Sending embed
                await ctx.send(embed=Embed)

                # Storing the start time of the duel
                startTime = datetime.datetime.now()

                # Deleting problem list
                del problemList

                # Waiting for the duel to end
                def check_3(m):
                    return m.content == "endduel" and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author)

                msg = await self.client.wait_for('message', check=check_3)

                async with ctx.typing():
                    # Obtaining and comparing the last submissions of the two users
                    async with session.get(f'https://codeforces.com/api/user.status?handle={handles[1]}&from=1&count=1') as r1:
                        async with session.get(f'https://codeforces.com/api/user.status?handle={handles[2]}&from=1&count=1') as r2:

                            # Saving the last submission in JSON form
                            data_1 = await r1.json()
                            data_2 = await r2.json()

                            # Boolean variables to check whether both users solved the problem
                            match_1 = False
                            match_2 = False

                            # Converting the timestamps to datetime objects
                            data_1["result"][0]["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
                                data_1["result"][0]["creationTimeSeconds"])
                            data_2["result"][0]["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
                                data_2["result"][0]["creationTimeSeconds"])

                            if int(problem[0]) == data_1["result"][0]["problem"]["contestId"] and data_1["result"][0]["creationTimeSeconds"] > startTime and problem[1] == data_1["result"][0]["problem"]["index"] and data_1["result"][0]["verdict"] == "OK":
                                match_1 = True
                            if int(problem[0]) == data_2["result"][0]["problem"]["contestId"] and data_2["result"][0]["creationTimeSeconds"] > startTime and problem[1] == data_2["result"][0]["problem"]["index"] and data_2["result"][0]["verdict"] == "OK":
                                match_2 = True

                # If both users solved the problem
                if match_1 and match_2:
                    if data_1["result"][0]["creationTimeSeconds"] <= data_2["result"][0]["creationTimeSeconds"]:
                        await ctx.send(f"<@{ctx.message.author.id}> has won the duel against <@{usr.id}>!")
                    else:
                        await ctx.send(f"<@{usr.id}> has won the duel against <@{ctx.message.author.id}>!")

                # If only user_1 solved the problem
                elif match_1:
                    await ctx.send(f"<@{ctx.message.author.id}> has won the duel against <@{usr.id}>!")

                # If only user_2 solved the problem
                elif match_2:
                    await ctx.send(f"<@{usr.id}> has won the duel against <@{ctx.message.author.id}>!")

                # If neither solved the problem
                else:
                    await ctx.send("Duel ended, neither won!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Duel ready!")


def setup(client):
    client.add_cog(Duel(client))
