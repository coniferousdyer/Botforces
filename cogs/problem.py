import discord
import aiohttp
import random
from discord.ext import commands


class Problem(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to suggest a random problem, with optional tags and rating
    @commands.command()
    async def problem(self, ctx, *args):
        async with aiohttp.ClientSession() as session:

            # Saving the URL as a string
            url = 'https://codeforces.com/api/problemset.problems'
            rating = 0
            check = False

            # Separating the rating and the tags
            for arg in args:
                if arg.isdigit():
                    rating = int(arg)
                else:
                    if not check:
                        url += '?tags={}'.format(arg)
                        check = True
                    else:
                        url += ';{}'.format(arg)

            async with session.get(url) as r:

                # If URL was not found
                if not r.ok:
                    await ctx.send("Sorry, an error occurred.")
                    return

                # Reading the data as JSON data and storing the dictionary in data variable
                data = await r.json()

                # Filtering out the problems without rating
                data["result"]["problems"] = filter(
                    lambda p: 'rating' in p, data["result"]["problems"])

                # If rating was given, i.e. rating != 0, then filter the list
                if rating != 0:
                    data["result"]["problems"] = filter(
                        lambda p: p["rating"] == rating, data["result"]["problems"])

                data["result"]["problems"] = list(data["result"]["problems"])

                # In case no problems are found
                if len(data["result"]["problems"]) == 0:
                    await ctx.send("Sorry, no problems could be found. Please try again.")
                    return

                # Storing problem
                problem = data["result"]["problems"][random.randint(
                    0, len(data["result"]["problems"]) - 1)]

                # Creating an embed
                Embed = discord.Embed(title="{}{}. {}".format(problem["contestId"], problem["index"], problem["name"]),
                                      url="https://codeforces.com/problemset/problem/{}/{}".format(
                                          problem["contestId"], problem["index"]),
                                      color=0xff0000)

                Embed.add_field(
                    name="Rating", value=problem["rating"], inline=False)

                # Formatting the strings in the list and joining them to form a string
                problem["tags"] = map(
                    lambda str: '||' + str + '||', problem["tags"])
                tags = ','.join(problem["tags"])
                Embed.add_field(name="Tags", value=tags)

                Embed.set_footer(icon_url=ctx.author.avatar_url,
                                 text=str(ctx.author))

                # Sending embed
                await ctx.send(embed=Embed)


def setup(client):
    client.add_cog(Problem(client))
