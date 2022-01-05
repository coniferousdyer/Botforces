import discord
import aiohttp
import asyncio
import sqlite3
import random
import datetime
from discord.ext import commands, tasks

from botforces.utils.constants import PROBLEM_WEBSITE_URL, SUBMISSION_URL


class Lockout(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lockout(self, ctx, usr: discord.User = None):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Checking if a user was mentioned
        if usr == None:
            await ctx.send(":x: Please mention whom you want to challenge.")
            return

        if usr.bot or usr == self.client.user:
            await ctx.send(":x: You can't challenge a bot.")
            return

        # Checking if the user mentioned themselves
        if usr == ctx.author:
            await ctx.send(":x: You can't challenge yourself.")
            return

        reactMsg = await ctx.send(f"<@{usr.id}>, react to this message with :thumbsup: within 30 seconds to accept the lockout challenge.")

        # Function to check the reaction on the message
        def check(reaction, user):
            return user == usr and str(reaction.emoji) == '\N{THUMBS UP SIGN}' and reactMsg.id == reaction.message.id

        # Waiting for the reaction
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(":x: Sorry, the challenge expired because 30 seconds were up!")
            return
        else:
            await ctx.send(f"<@{usr.id}> has accepted the challenge! Send handles of <@{ctx.message.author.id}> and <@{usr.id}> respectively like this within the next 60 seconds:\n```handles <handle of {ctx.author.display_name}> <handle of {usr.display_name}>```")

            def check_2(m):
                return m.content.startswith("handles") and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author) and len(m.content.split()) == 3

            try:
                msg = await self.client.wait_for('message', timeout=60.0, check=check_2)
            except asyncio.TimeoutError:
                await ctx.send(":x: Sorry, the challenge expired because 60 seconds were up!")
                return
            else:
                await ctx.send(f"Send the problem ratings you would like like this in the next 60 seconds:\n```ratings <rating_1> <rating_2> <rating_3> <rating_4> <rating_5>```")
                # handles is a list that stores the two handles
                handles = msg.content.split()

                def check_3(m):
                    return m.content.startswith("ratings") and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author) and len(m.content.split()) == 6

                try:
                    msg = await self.client.wait_for('message', timeout=60.0, check=check_3)
                except asyncio.TimeoutError:
                    await ctx.send(":x: Sorry, the challenge expired because 60 seconds were up!")
                    return
                else:
                    await ctx.send("Send the points of each problem in order like this in the next 60 seconds:\n```points <points_1> <points_2> <points_3> <points_4> <points_5>```")
                    # ratings is a list that stores the problem ratings
                    ratings = msg.content.split()

                    def check_4(m):
                        return m.content.startswith("points") and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author) and len(m.content.split()) == 6

                    try:
                        msg = await self.client.wait_for('message', timeout=60.0, check=check_4)
                    except asyncio.TimeoutError:
                        await ctx.send(":x: Sorry, the challenge expired because 60 seconds were up!")
                        return
                    else:
                        await ctx.send("Send the duration of the challenge (between 5-180) like this in the next 60 seconds:\n```duration <number>```")
                        # points is a list that stores the points of each problem
                        points = msg.content.split()

                        def check_5(m):
                            return m.content.startswith("duration") and m.channel == reactMsg.channel and (m.author == usr or m.author == ctx.message.author) and len(m.content.split()) == 2 and int(m.content.split()[1]) >= 5 and int(m.content.split()[1]) <= 180

                        try:
                            msg = await self.client.wait_for('message', timeout=60.0, check=check_5)
                        except asyncio.TimeoutError:
                            await ctx.send(":x: Sorry, the challenge expired because 60 seconds were up!")
                            return
                        else:
                            await ctx.send("Starting lockout challenge...")
                            # duration stores the duration of the match
                            duration = msg.content.split()

                            async with ctx.typing():
                                # Opening data.db and reading the problems into a list
                                connection = sqlite3.connect("data.db")
                                cursor = connection.cursor()

                                # Defining a string that contains the problems
                                problem_string = ''
                                problems = []
                                count = 1

                                # Searching for the problems
                                for rating in ratings:
                                    if rating != "ratings":

                                        # Finding problems of given rating
                                        tempList = cursor.execute(
                                            "SELECT * FROM problems WHERE rating = ?", (rating,)).fetchall()

                                        # In case no problems are found
                                        if len(tempList) == 0:
                                            await ctx.send(f":x: Sorry, a problem of rating {rating} could not be found. Please try again.")
                                            return

                                        # Storing problem
                                        problem = tempList[random.randint(
                                            0, len(tempList) - 1)]

                                        problems.append(problem)

                                        problem_string += f"{count}. [{problem[2]} - {ratings[count]}]({PROBLEM_WEBSITE_URL}{problem[0]}/{problem[1]}) - {points[count]} points\n"
                                        count += 1

                                # Defining the 2-sized list which stores points of both users
                                userPoints = [0, 0]

                                # Creating embed
                                Embed = discord.Embed(title=f"{ctx.author.display_name} vs {usr.display_name}",
                                                      description=problem_string,
                                                      color=0xff0000)

                                Embed.add_field(
                                    name=f"Points for {ctx.author.display_name}", value=userPoints[0])
                                Embed.add_field(
                                    name=f"Points for {usr.display_name}", value=userPoints[1])

                                # Storing the start time of the challenge
                                startTime = datetime.datetime.now()

                                # Displaying time left
                                m, s = divmod(
                                    ((startTime + datetime.timedelta(minutes=int(duration[1]))) - startTime).total_seconds(), 60)
                                h = int(m//60)
                                m = int(m % 60)
                                dateString = 'Time left: '

                                if h != 0:
                                    dateString += f"{h} hours, "
                                if m != 0:
                                    dateString += f"{m} minutes"

                                Embed.set_footer(text=dateString)

                            # Sending embed and closing connection
                            await ctx.send(embed=Embed)
                            connection.close()

                            # Storing the sum of the points to know when a match gets over
                            sumPoints = 0
                            for point in points:
                                if point != "points":
                                    sumPoints += int(point)

                            # Defining a background task to check the submissions of each user
                            @tasks.loop(seconds=30)
                            async def checkSubmissions():
                                async with aiohttp.ClientSession() as session:
                                    # Obtaining and comparing the last submissions of the two users
                                    async with session.get(f'{SUBMISSION_URL}{handles[1]}&from=1&count=1') as r1:
                                        async with session.get(f'{SUBMISSION_URL}{handles[2]}&from=1&count=1') as r2:

                                            # Saving the last submission in JSON form
                                            data_1 = await r1.json()
                                            data_2 = await r2.json()

                                    # Boolean variables to check whether both users solved the problem
                                    match_1 = -1
                                    match_2 = -1

                                    # Converting the timestamps to datetime objects
                                    data_1["result"][0]["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
                                        data_1["result"][0]["creationTimeSeconds"])
                                    data_2["result"][0]["creationTimeSeconds"] = datetime.datetime.fromtimestamp(
                                        data_2["result"][0]["creationTimeSeconds"])

                                    # Iterating through the problems
                                    for i in range(5):
                                        if problems[i] != None and int(problems[i][0]) == data_1["result"][0]["problem"]["contestId"] and data_1["result"][0]["creationTimeSeconds"] > startTime and problems[i][1] == data_1["result"][0]["problem"]["index"] and data_1["result"][0]["verdict"] == "OK":
                                            match_1 = i
                                        if problems[i] != None and int(problems[i][0]) == data_2["result"][0]["problem"]["contestId"] and data_2["result"][0]["creationTimeSeconds"] > startTime and problems[i][1] == data_2["result"][0]["problem"]["index"] and data_2["result"][0]["verdict"] == "OK":
                                            match_2 = i

                                    # Both users solved the same problem
                                    if match_1 != -1 and match_2 != -1 and match_1 == match_2:
                                        if data_1["result"][0]["creationTimeSeconds"] <= data_2["result"][0]["creationTimeSeconds"]:
                                            userPoints[0] += int(
                                                points[match_1 + 1])
                                            problems[match_1] = None
                                            await ctx.send(f"UPDATE: <@{ctx.message.author.id}> gained {points[match_1 + 1]} points! <@{ctx.message.author.id}> <@{usr.id}>")
                                        else:
                                            userPoints[1] += int(
                                                points[match_1 + 1])
                                            problems[match_2] = None
                                            await ctx.send(f"UPDATE: <@{usr.id}> gained {points[match_2 + 1]} points! <@{ctx.message.author.id}> <@{usr.id}>")

                                    # If the users solved different problems
                                    elif match_1 != -1 and match_2 != -1 and match_1 != match_2:
                                        userPoints[0] += int(points[match_1 + 1])
                                        userPoints[1] += int(points[match_2 + 1])
                                        problems[match_1] = None
                                        problems[match_2] = None
                                        await ctx.send(f"UPDATE: <@{ctx.message.author.id}> gained {points[match_1 + 1]} points and <@{usr.id}> gained {points[match_2 + 1]} points! <@{ctx.message.author.id}> <@{usr.id}>")

                                    # If only user 1 solved a problem
                                    elif match_1 != -1:
                                        userPoints[0] += int(points[match_1 + 1])
                                        problems[match_1] = None
                                        await ctx.send(f"UPDATE: <@{ctx.message.author.id}> gained {points[match_1 + 1]} points! <@{ctx.message.author.id}> <@{usr.id}>")

                                    # If only user 2 solved a problem
                                    elif match_2 != -1:
                                        userPoints[1] += int(points[match_2 + 1])
                                        problems[match_2] = None
                                        await ctx.send(f"UPDATE: <@{usr.id}> gained {points[match_2 + 1]} points! <@{ctx.message.author.id}> <@{usr.id}>")

                                    # Sending embed only if a problem was solved
                                    if match_1 != -1 or match_2 != -1:
                                        count = 1
                                        problem_string = ''
                                        for problem in problems:
                                            if problem != None:
                                                problem_string += f"{count}. [{problem[2]} - {ratings[count]}]({PROBLEM_WEBSITE_URL}{problem[0]}/{problem[1]}) - {points[count]} points\n"
                                            else:
                                                problem_string += f"{count}. Solved - {points[count]} points\n"
                                            count += 1

                                        # Obtaining current time and thus time left
                                        currentTime = datetime.datetime.now()
                                        m, s = divmod(
                                            ((startTime + datetime.timedelta(minutes=int(duration[1]))) - currentTime).total_seconds(), 60)
                                        h = int(m//60)
                                        m = int(m % 60)
                                        dateString = 'Time left: '

                                        if h != 0:
                                            dateString += f"{h} hours, "
                                        if m != 0:
                                            dateString += f"{m} minutes, "
                                        dateString += f"{int(s)} seconds"

                                        # Creating embed
                                        Embed = discord.Embed(title=f"{ctx.author.display_name} vs {usr.display_name}",
                                                              description=problem_string,
                                                              color=0xff0000)

                                        Embed.add_field(
                                            name=f"Points for {ctx.author.display_name}", value=userPoints[0])
                                        Embed.add_field(
                                            name=f"Points for {usr.display_name}", value=userPoints[1])

                                        Embed.set_footer(text=dateString)

                                        # Sending embed
                                        await ctx.send(embed=Embed)

                            # Starting the background task
                            checkSubmissions.start()

                            def check_6(m):
                                return m.content.startswith("UPDATE:") and msg.author == self.client.user and userPoints[0] + userPoints[1] == sumPoints

                            try:
                                msg = await self.client.wait_for('message', timeout=(int(duration[1]) * 60.0) + 5, check=check_6)
                            except asyncio.TimeoutError:
                                await ctx.send(f"Time up! Match ended! <@{ctx.message.author.id}> <@{usr.id}>")
                            else:
                                await ctx.send(f"All problems solved! Match ended! <@{ctx.message.author.id}> <@{usr.id}>")

                            # Stopping the background task
                            checkSubmissions.stop()
                            Embed = discord.Embed(
                                title="Final Standings", color=0xff0000)

                            # Determining the winner
                            if userPoints[0] > userPoints[1]:
                                Embed.add_field(
                                    name="Result", value=f"{ctx.author.display_name} wins!", inline=False)
                                Embed.add_field(
                                    name=f":first_place: {ctx.author.display_name}", value=userPoints[0])
                                Embed.add_field(
                                    name=f":second_place: {usr.display_name}", value=userPoints[1])

                            elif userPoints[0] < userPoints[1]:
                                Embed.add_field(
                                    name="Result", value=f"{usr.display_name} wins!", inline=False)
                                Embed.add_field(
                                    name=f":first_place: {usr.display_name}", value=userPoints[1])
                                Embed.add_field(
                                    name=f":second_place: {ctx.author.display_name}", value=userPoints[0])

                            else:
                                Embed.add_field(
                                    name="Result", value=f"Draw", inline=False)
                                Embed.add_field(
                                    name=f":first_place: {ctx.author.display_name}", value=userPoints[0])
                                Embed.add_field(
                                    name=f":first_place: {usr.display_name}", value=userPoints[1])

                            # Sending result embed
                            await ctx.send(embed=Embed)

                            ########## ADD TIMES ALSO ##########

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Lockout ready!")


def setup(client):
    client.add_cog(Lockout(client))
