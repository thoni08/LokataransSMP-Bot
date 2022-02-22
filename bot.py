import asyncio
import discord
import os

from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
from python_aternos import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    await self.bot.change_presence(status=discord.Status.idle)
    print('bot ready')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

try:
    bot.run(os.environ['TOKEN'])
except:
    bot.run(os.environ.get('TOKEN'))