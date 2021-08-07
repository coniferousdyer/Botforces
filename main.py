import discord
import json
import aiohttp
from discord.ext import commands

client = commands.Bot(command_prefix='-')

TOKEN = ''
with open("token.json") as f:
    TOKEN = json.load(f)
    TOKEN = TOKEN["token"]


@client.event
async def on_ready():
    print("Bot is online!")


@client.command()
async def search(ctx, handle):
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
                                  description="Rank: {}\nRating: {}".format(
                                      data["result"][0]["rank"], data["result"][0]["rating"]),
                                  color=color)

            # Sending the embed
            await ctx.send(embed=Embed)


@client.command()
async def stalk(ctx, handle, number=10):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/user.status?handle={}&from=1&count={}'.format(handle, number)) as r:

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

            # Sending the embed
            await ctx.send(embed=Embed)

client.run(TOKEN)
