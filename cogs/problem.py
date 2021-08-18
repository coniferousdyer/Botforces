import discord
import csv
import random
import aiohttp
from discord.ext import commands


class Problem(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to suggest a random problem, with optional tags and rating
    @commands.command()
    async def problem(self, ctx, *args):

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
            await ctx.send("Sorry, no problems could be found. Please try again.")
            return

        # Storing problem
        problem = problemList[random.randint(0, len(problemList) - 1)]

        # Creating an embed
        Embed = discord.Embed(title=f"{problem[0]}{problem[1]}. {problem[2]}",
                              url=f"https://codeforces.com/problemset/problem/{problem[0]}/{problem[1]}",
                              color=0xff0000)

        Embed.add_field(
            name="Rating", value=problem[4], inline=False)

        # Formatting the strings in the list and joining them to form a string
        problem[3] = map(
            lambda str: '||' + str + '||', problem[3])
        tags = ','.join(problem[3])
        Embed.add_field(name="Tags", value=tags)

        Embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=str(ctx.author))

        # Sending embed
        await ctx.send(embed=Embed)

    @commands.Cog.listener()
    async def on_ready(self):

        async with aiohttp.ClientSession() as session:
            async with session.get('https://codeforces.com/api/problemset.problems') as r:

                # Reading the contests list as JSON data
                data = await r.json()
                data["result"]["problems"] = filter(
                    lambda p: 'rating' in p, data["result"]["problems"])

                with open('data/problems.csv', 'w') as csvFile:
                    csvWriter = csv.writer(csvFile, delimiter=',')
                    for p in data["result"]["problems"]:
                        p['tags']
                        csvWriter.writerow([p['contestId'], p['index'],
                                            p['name'], p['tags'], p['rating']])

        print("-Problem ready!")


def setup(client):
    client.add_cog(Problem(client))
