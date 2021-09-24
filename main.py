import discord
import os
import aiohttp
import sqlite3
from discord.ext import tasks, commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix='-', help_command=None)

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

cogs = ['cogs.help', 'cogs.user', 'cogs.stalk',
        'cogs.problem', 'cogs.upcoming', 'cogs.duel', 'cogs.plot', 'cogs.error', 'cogs.lockout']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as exc:
        print(f"Could not load cog {cog}: {str(exc)}")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Codeforces"))
    reload_cogs.start()

    # Creating a duels table to store information about ongoing duels
    connection = sqlite3.connect("data/data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS duels")
    cursor.execute("CREATE TABLE duels(user1_id BIGINT, user2_id BIGINT, startTime DATETIME, contestId INTEGER, contestIndex TEXT, handle1 TEXT, handle2 TEXT)")
    connection.commit()
    connection.close()

    print("Bot is online!")


@tasks.loop(hours=1)
async def reload_cogs():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/contest.list') as r:

            # Reading the contests list as JSON data
            data = await r.json()

            # Storing the upcoming contests in data.db
            connection = sqlite3.connect("data/data.db")
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS contests")
            cursor.execute("CREATE TABLE contests(id INTEGER, name TEXT, durationSeconds BIGINT, startTimeSeconds BIGINT)")
            for c in data['result']:
                if c['phase'] == "BEFORE":
                    cursor.execute("INSERT INTO contests VALUES(?, ?, ?, ?)", (c['id'], c['name'], c['durationSeconds'], c['startTimeSeconds']))
                else:
                    break

    async with aiohttp.ClientSession() as session:
        async with session.get('https://codeforces.com/api/problemset.problems') as r:

            # Reading the contests list as JSON data
            data = await r.json()
            data["result"]["problems"] = filter(
                lambda p: 'rating' in p, data["result"]["problems"])

            # Storing the problems in data.db
            cursor.execute("DROP TABLE IF EXISTS problems")
            cursor.execute("CREATE TABLE problems(contestId INTEGER, contestIndex TEXT, name TEXT, tags TEXT, rating INTEGER)")
            for p in data["result"]["problems"]:
                cursor.execute("INSERT INTO problems VALUES(?, ?, ?, ?, ?)", (p['contestId'], p['index'], p['name'], repr(p['tags']), p['rating']))
            
            connection.commit()
            connection.close()


client.run(TOKEN)
