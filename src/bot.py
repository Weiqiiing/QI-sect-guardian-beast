# -*- coding: utf-8 -*-
import discord
import os
from discord.ext import commands
from discord.ext.commands import Bot
from src import config


bot = commands.Bot(command_prefix=os.environ['BOT_PREFIX'])

config.init()

startup_extensions = ["commands.fun", "commands.sect",
                      "utils.events", "utils.roles", "XP.xp"]

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(os.environ['BOT_TOKEN'])

# Made by Weiqing#2360 & Perpetual Phoenix#0363
