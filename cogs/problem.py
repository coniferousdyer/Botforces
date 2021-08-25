import discord
import csv
import random
from discord.ext import commands


class Problem(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to suggest a random problem, with optional tags and rating
    @commands.command()
    async def problem(self, ctx, *args):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

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
                              color=0xff0000)

        Embed.add_field(
            name="Rating", value=problem[4], inline=False)

        # Formatting the strings in the list and joining them to form a string
        if problem[3] != []:  
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
        print("-Problem ready!")


def setup(client):
    client.add_cog(Problem(client))
