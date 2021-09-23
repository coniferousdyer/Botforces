from sqlite3.dbapi2 import connect
import discord
import sqlite3
import random
from discord.ext import commands
from discord.ext.commands.core import check


class Problem(commands.Cog):
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
    async def problem(self, ctx, *args):

        # Checking if the author was a bot
        if ctx.message.author == self.client.user or ctx.message.author.bot:
            return

        # Separating the rating and the tags
        rating = 0
        tags = []
        for arg in args:
            if arg.isdigit():
                rating = int(arg)
            else:
                tags.append(arg)

        # Opening data.db and reading the problems of rating (if mentioned) into a list
        connection = sqlite3.connect("data/data.db")
        cursor = connection.cursor()
        if rating != 0:
            problemList = cursor.execute(
                "SELECT * FROM problems WHERE rating = ?", (rating,)).fetchall()
        else:
            problemList = cursor.execute("SELECT * FROM problems").fetchall()

        # If tags were given, i.e. tags is not empty, check tags and add it to the final list
        finalList = []
        if tags != []:
            for problem in problemList:
                if self.check_tags(problem[3], tags):
                    finalList.append(problem)

        # In case no problems are found
        problemList = finalList
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

        # Printing the tags in spoilers
        if problem[3] != "[]":
            tags = problem[3].split(", ")
            tags = [tag.strip("[]\'") for tag in tags]
            tags = map(lambda str: '||' + str + '||', tags)
            tags = ','.join(tags)
            Embed.add_field(name="Tags", value=tags)

        Embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=str(ctx.author))

        # Sending embed
        await ctx.send(embed=Embed)
        connection.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("-Problem ready!")


def setup(client):
    client.add_cog(Problem(client))
