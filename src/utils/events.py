import discord
from discord.ext import commands
import datetime
import time
from src import config


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print("_____________________\nSect XP Tracking On")
        await self.bot.change_presence(game=discord.Game(name="the Chat :shy:", type=3))


def setup(bot):
    bot.add_cog(Events(bot))
