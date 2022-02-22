import discord

from discord.ext import commands
from discord.utils import get
from discord.ext.commands import bot
from discord.ext.commands import check
from discord.ext.commands import cooldown
from discord.ext.commands import BucketType
from discord.ext.commands import (CommandOnCooldown, CommandNotFound)

from dotenv import load_dotenv
from os.path import join, dirname
from python_aternos import Client

try:
    aternos = Client(os.environ['ATERNOS_USERNAME'], password=os.environ['ATERNOS_PASSWORD'])
except:
    aternos = Client(os.environ.get('ATERNOS_USERNAME'), password=os.environ.get('ATERNOS_PASSWORD'))

atservers = aternos.servers
myserv = atservers[0]

class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} ready")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandOnCooldown):
            await ctx.send(f"karena cooldown di share satu server, tunggu **{exc.retry_after:.0f} detik** lagi terus ketik ulang")
        elif isinstance(exc, CommandNotFound):
            await ctx.send("command tidak ditemukan")

    @commands.slash_command()
    @cooldown(1, 60, BucketType.guild)
    async def turnon(ctx):

        # Get Status before turning on
        try:
            status = myserv.status
        except:
            await ctx.send("Error: Cannot get server status, please check bot console for more info.")
            print("Error: Cannot get server status")

        # Status Check
        if status == 0:
            # Try to start
            try:
                myserv.start()
                await ctx.send("server otw nyala, tunggu bentar ya")
            except:
                await ctx.send("Error: Failed to start server, please check bot console for more info.")

        elif status == 1:
            await ctx.send("server udah nyala wth")

        else:
            await ctx.send("harusnya servernya udah nyala sih, kalo belum ya... gatau lah wkwk")
        
def setup(bot):
    bot.add_cog(commands(bot))