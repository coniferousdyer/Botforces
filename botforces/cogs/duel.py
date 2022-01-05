import discord
import aiohttp
import asyncio
import sqlite3
import random
import datetime
from discord.ext import commands


class Duel(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Function to check if all tags are present
    def check_tags(self, problem_tags, tags):
        count = 0
        for tag in tags:
            if "\'" + tag + "\'" in problem_tags:
                count += 1

        return count == len(tags)

    # Command to suggest a random problem, with optional tags and rating
    @commands.command()
    async def duel(self, ctx, usr: discord.User = None, *args):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

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

            # Initialising rating to 0 and tags to empty list
            rating = 0
            tags = []

            # Separating the rating and the tags
            for arg in args:
                if arg.isdigit():
                    rating = int(arg)
                else:
                    tags.append(arg)

            # Opening data.db and reading the problems into a list
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            if rating != 0:
                problemList = cursor.execute(
                    "SELECT * FROM problems WHERE rating = ?", (rating,)).fetchall()
            else:
                problemList = cursor.execute(
                    "SELECT * FROM problems").fetchall()

            # If tags were given, i.e. tags is not empty, check tags and add it to the final list
            finalList = []
            if tags != []:
                for problem in problemList:
                    if self.check_tags(problem[3], tags):
                        finalList.append(problem)

                problemList = finalList

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

            # Printing the tags in spoilers
            if problem[3] != "[]":
                tags = problem[3].split(", ")
                tags = [tag.strip("[]\'") for tag in tags]
                tags = map(lambda str: '||' + str + '||', tags)
                tags = ','.join(tags)
                Embed.add_field(name="Tags", value=tags)

            Embed.add_field(
                name="Duel", value=f"{ctx.author.display_name} vs {usr.display_name}", inline=False)

            # Sending embed
            await ctx.send(embed=Embed)

            # Storing the start time of the duel
            startTime = datetime.datetime.now()

            # Storing the duel details in data.db
            cursor.execute("INSERT INTO duels VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (ctx.message.author.id, usr.id, startTime, problem[0], problem[1], handles[1], handles[2]))
            connection.commit()
            connection.close()

    # Command to conclude the duel and declare the winner
    @commands.command()
    async def endduel(self, ctx):

        # Searching duels in data.db to find the one which message author is part of
        connection = sqlite3.connect("data/data.db")
        cursor = connection.cursor()
        duel = cursor.execute("SELECT * FROM duels WHERE user1_id = ? OR user2_id = ?",
                              (ctx.message.author.id, ctx.message.author.id)).fetchone()

        # If no duel with the user was found
        if duel == None:
            await ctx.send("You are not taking part in a duel currently!")
            connection.close()
            return

        async with aiohttp.ClientSession() as session:
            async with ctx.typing():
                # Obtaining and comparing the last submissions of the two users
                async with session.get(f'https://codeforces.com/api/user.status?handle={duel[5]}&from=1&count=1') as r1:
                    async with session.get(f'https://codeforces.com/api/user.status?handle={duel[6]}&from=1&count=1') as r2:

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

                        startTime = datetime.datetime.strptime(
                            duel[2], "%Y-%m-%d %H:%M:%S.%f")
                        if duel[3] == data_1["result"][0]["problem"]["contestId"] and data_1["result"][0]["creationTimeSeconds"] > startTime and duel[4] == data_1["result"][0]["problem"]["index"] and data_1["result"][0]["verdict"] == "OK":
                            match_1 = True
                        if duel[3] == data_2["result"][0]["problem"]["contestId"] and data_2["result"][0]["creationTimeSeconds"] > startTime and duel[4] == data_2["result"][0]["problem"]["index"] and data_2["result"][0]["verdict"] == "OK":
                            match_2 = True

        # If both users solved the problem
        if match_1 and match_2:
            if data_1["result"][0]["creationTimeSeconds"] <= data_2["result"][0]["creationTimeSeconds"]:
                await ctx.send(f"<@{duel[0]}> has won the duel against <@{duel[1]}>!")
            else:
                await ctx.send(f"<@{duel[1]}> has won the duel against <@{duel[0]}>!")

        # If only user_1 solved the problem
        elif match_1:
            await ctx.send(f"<@{duel[0]}> has won the duel against <@{duel[1]}>!")

        # If only user_2 solved the problem
        elif match_2:
            await ctx.send(f"<@{duel[1]}> has won the duel against <@{duel[0]}>!")

        # If neither solved the problem
        else:
            usrId = None
            if ctx.message.author.id == duel[0]:
                usrId = duel[1]
            else:
                usrId = duel[0]

            reactMsg = await ctx.send(f"<@{usrId}>, react to this message with :thumbsup: within 30 seconds to invalidate the duel.")

            # Function to check the reaction on the message
            def check_3(reaction, user):
                return user.id == usrId and str(reaction.emoji) == '\N{THUMBS UP SIGN}' and reactMsg.id == reaction.message.id

            # Waiting for the reaction
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check_3)
            except asyncio.TimeoutError:
                await ctx.send(":x: Sorry, the invalidation request expired because 30 seconds were up!")
                connection.close()
                return
            else:
                await ctx.send("Duel ended, neither won!")
                cursor.execute("DELETE FROM duels WHERE user1_id = ? AND user2_id = ? AND startTime = ? AND contestId = ? AND contestIndex = ? AND handle1 = ? AND handle2 = ?",
                               (duel[0], duel[1], duel[2], duel[3], duel[4], duel[5], duel[6]))
                connection.commit()
                connection.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Duel ready!")


def setup(client):
    client.add_cog(Duel(client))
