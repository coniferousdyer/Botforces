import discord
import os
import aiohttp
import csv
from discord.ext import tasks, commands
from discord.ext.commands import bot
from dotenv import load_dotenv

client = commands.Bot(command_prefix='-', help_command=None)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

cogs = ['cogs.help', 'cogs.user', 'cogs.stalk',
        'cogs.problem', 'cogs.upcoming', 'cogs.duel', 'cogs.plot']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as exc:
        print(f"Could not load cog {cog}: {str(exc)}")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Codeforces"))
    reload_cogs.start()
    print("Bot is online!")


@tasks.loop(hours=1)
async def reload_cogs():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/contest.list') as r:

            # Reading the contests list as JSON data
            data = await r.json()

            # Storing the upcoming contests in contests.csv
            with open("data/contests.csv", "w") as csvFile:
                csvWriter = csv.writer(csvFile, delimiter=",")
                for c in data['result']:
                    if c['phase'] == "BEFORE":
                        csvWriter.writerow(
                            [c['id'], c['name'], c['durationSeconds'], c['startTimeSeconds']])
                    else:
                        break

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


client.run(TOKEN)
