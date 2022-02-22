import asyncio
import discord
import os

from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
from python_aternos import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

try:
    aternos = Client(os.environ['ATERNOS_USERNAME'], password=os.environ['ATERNOS_PASSWORD'])
except:
    aternos = Client(os.environ.get('ATERNOS_USERNAME'), password=os.environ.get('ATERNOS_PASSWORD'))

atservers = aternos.servers
myserv = atservers[0]

bot = commands.Bot(command_prefix="!", case_insensitive=True)

@bot.event
async def on_ready():
    print('bot ready')

async def activity():
    await bot.wait_until_ready()

    while not bot.is_closed():
        status = int(myserv.status)
        if status != 1:
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Not Minecraft"))
        await asyncio.sleep(10)

bot.loop.create_task(activity())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

try:
    bot.run(os.environ['TOKEN'])
except:
    bot.run(os.environ.get('TOKEN'))