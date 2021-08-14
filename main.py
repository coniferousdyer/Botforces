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

cogs = ['cogs.user', 'cogs.stalk', 'cogs.problem', 'cogs.upcoming']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as exc:
        print(f"Could not load cog {cog}: {str(exc)}")


@client.event
async def on_ready():
    print("Bot is online!")


client.run(TOKEN)
