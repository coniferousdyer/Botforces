import discord
import json
import aiohttp
import random
import datetime
import time
from discord.ext import commands

client = commands.Bot(command_prefix='-')

TOKEN = ''
with open("token.json") as f:
    TOKEN = json.load(f)
    TOKEN = TOKEN["token"]


@client.event
async def on_ready():
    print("Bot is online!")


# Command to search for a user and display their basic details
@client.command()
async def user(ctx, handle):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/user.info?handles={}'.format(handle)) as r:

            # If the user was not found
            if not r.ok:
                await ctx.send("Sorry, user with handle {} could not be found.".format(handle))
                return

            # Reading the data as JSON data and storing the dictionary in data variable
            data = await r.json()

            # Assigning a color according to rank
            color = 0xff0000
            if data["result"][0]["rank"] == "newbie":
                color = 0x918f8e
            elif data["result"][0]["rank"] == "pupil":
                color = 0x087515
            elif data["result"][0]["rank"] == "specialist":
                color = 0x1af2f2
            elif data["result"][0]["rank"] == "expert":
                color = 0x1300f9
            elif data["result"][0]["rank"] == "candidate master":
                color = 0xb936ee
            elif data["result"][0]["rank"] == "master" or data["result"][0]["rank"] == "international master":
                color = 0xeebb36

            # Creating an embed
            Embed = discord.Embed(title=data["result"][0]["handle"],
                                  url="https://codeforces.com/profile/{}".format(
                                      data["result"][0]["handle"]),
                                  color=color)

            Embed.set_thumbnail(url=data["result"][0]["avatar"])

            if 'firstName' in data["result"][0] and 'lastName' in data["result"][0]:
                Embed.add_field(
                    name="Name", value=data["result"][0]["firstName"] + ' ' + data["result"][0]["lastName"], inline=False)

            if 'city' in data["result"][0] and 'country' in data["result"][0]:
                Embed.add_field(
                    name="City", value=data["result"][0]["city"] + ', ' + data["result"][0]["country"], inline=False)

            Embed.add_field(
                name="Rank", value=data["result"][0]["rank"].title(), inline=False)
            Embed.add_field(name="Rating",
                            value=data["result"][0]["rating"], inline=False)

            Embed.set_footer(icon_url=ctx.author.avatar_url, text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)


# ERROR HANDLING TO BE DONE - ALL ACS ONLY + PROBLEMS WITH NO RATINGS
# Command to display the last n submissions of a user
@ client.command()
async def stalk(ctx, handle, number=10):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/user.status?handle={}&count={}'.format(handle, number)) as r:

            # If user was not found
            if not r.ok:
                await ctx.send("Sorry, user with handle {} could not be found.".format(handle))
                return

            # Reading the data as JSON data and storing the dictionary in data variable
            data = await r.json()

            # Creating the string of submissions to be the description of Embed
            submissions = ''
            count = 1
            for problem in data["result"]:
                if count == number:
                    submissions += "{}. {} - {} ({})".format(
                        count, problem["problem"]["name"], problem["problem"]["rating"], problem["verdict"])
                else:
                    submissions += "{}. {} - {} ({})\n".format(
                        count, problem["problem"]["name"], problem["problem"]["rating"], problem["verdict"])
                count += 1

            # Creating an embed
            Embed = discord.Embed(
                title="Last {} submissions of {}".format(number, handle),
                description=submissions,
                color=0xff0000)

            Embed.set_footer(icon_url=ctx.author.avatar_url, text=str(ctx.author))

            # Sending the embed
            await ctx.send(embed=Embed)


# Command to suggest a random problem, with optional tags and rating
@client.command()
async def problem(ctx, *args):
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

            Embed.set_footer(icon_url=ctx.author.avatar_url, text=str(ctx.author))

            # Sending embed
            await ctx.send(embed=Embed)


# Command to display upcoming contests
@client.command()
async def upcoming(ctx):
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

                Embed.set_footer(icon_url=ctx.author.avatar_url, text=str(ctx.author))

            # Sending embed
            await ctx.send(embed=Embed)

client.run(TOKEN)
