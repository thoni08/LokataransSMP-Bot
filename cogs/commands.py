import discord
import os

from discord.ext import commands, tasks
from discord.utils import get
from discord.ext.commands import bot
from discord.ext.commands import check
from discord.ext.commands import cooldown
from discord.ext.commands import BucketType
from discord.ext.commands import (CommandOnCooldown, CommandNotFound)

from dotenv import load_dotenv
from os.path import join, dirname
from python_aternos import Client

# Try to login to Aternos
aternos = None
while aternos is None:
    try:
        try:
            aternos = Client(str(os.environ['ATERNOS_USERNAME']), password=str(os.environ['ATERNOS_PASSWORD']))
        except:
            aternos = Client(str(os.environ.get('ATERNOS_USERNAME')), password=str(os.environ.get('ATERNOS_PASSWORD')))
    except:
        print("Failed to login. Retrying...")
        pass

atservers = None
while atservers is None:
    try:
        atservers = aternos.servers
    except:
        print("Failed to get server information.")
        pass

myserv = atservers[0]

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Start change_presence loop
        self.change_presence.start()

        # Print if ready
        print(f"{os.path.basename(__file__)} ready")
    
    @tasks.loop(seconds=10.0)
    async def change_presence(self):
        while True:
            try:
                status_forpresence = int(myserv.status)
            except SyntaxError:
                print("Unable to get status.")
            except:
                print("Unable to get status.")
                pass
            break

        if status_forpresence == 0:
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("Not Minecraft"))
        else:
            await self.bot.change_presence(activity=discord.Game("Minecraft"))
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(f"karena cooldown di share satu server, tunggu **{exc.retry_after:.0f} detik** lagi terus ketik ulang")
        elif isinstance(exc, CommandNotFound):
            await ctx.send("command tidak ditemukan")

    @commands.command(aliases=['on'])
    @cooldown(1, 60, BucketType.guild)
    async def turnon(self, ctx):
        # Get Status before turning on
        status = None
        while status is None:
            try:
                status = int(myserv.status)
            except:
                await ctx.send("Error: Cannot get server status, please check bot console for more info.")
                print("Error: Cannot get server status.")
                pass

        # Status Check
        if status == 0:
            # Try to start
            while True:
                try:
                    myserv.start()
                    await ctx.send("server otw nyala, tunggu bentar ya")
                except SyntaxError:
                    await ctx.send("Error: Failed to start server, please check bot console for more info.")
                except:
                    continue
                break

        elif status == 1:
            await ctx.send("server udah nyala wth")
        
        elif status == 2:
            await ctx.send("sabar masih loading")

        else:
            await ctx.send("harusnya servernya udah nyala sih, kalo belum ya... gatau lah wkwk")
        status = None

        print(f'{ctx.message.author} executed "turnon"')
        
def setup(bot):
    bot.add_cog(commands(bot))