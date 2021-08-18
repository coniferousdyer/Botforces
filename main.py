import discord
import os
from discord import activity
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv

client = commands.Bot(command_prefix='-')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

cogs = ['cogs.user', 'cogs.stalk', 'cogs.problem', 'cogs.upcoming', 'cogs.duel']

for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as exc:
        print(f"Could not load cog {cog}: {str(exc)}")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Codeforces"))
    print("Bot is online!")


client.run(TOKEN)
