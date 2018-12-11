import discord
from discord.ext import commands
from src import config
from src.XP.fileUpdate import *
from src.data.sectInfo import *
import csv
import asyncio
import random
import datetime
import time


class XP:
    def __init__(self, bot):
        self.bot = bot
        self.sectXP = config.sectXP
        self.sectLvl = config.sectLvl
        self.xpban = config.xpban

    async def on_message(self, message):
        if message.channel.id == "326959934187110402":
            pass
        else:
            try:
                located = False

                search = message.author.id
                for idCheck in self.xpban:
                    if search in idCheck:
                        located = True
                if message.author.nick is None or located == True:
                    pass

                else:
                    # Add another list for new user  ["",""]
                    self.xpban += [[""] * 2]
                    # Add userID to new sectList     ["userID",""]
                    self.xpban[len(self.xpban) - 2][0] = (message.author.id)
                    # Add the second value           ["userID", "second"]
                    self.xpban[len(self.xpban) - 2][1] = (a.second)

                    for tag in range(len(sectCall)):
                        if sectTags[tag].upper() in message.author.nick.upper():
                            self.sectXP[tag] += random.randint(2, 5)  # set xp
                            print(str(sectList[tag]) +
                                  " = " + str(self.sectXP[tag]) + "xprin")
                            writeFile("levels.csv", "w", self.sectXP)

                    for xpCheck in range(len(sectCall)):
                        if self.sectXP[xpCheck] >= requiredXP[self.sectLvl[xpCheck]]:
                            self.sectXP[xpCheck] = 0
                            self.sectLvl[xpCheck] += 1
                            writeFile("sectLevels.csv", "w", self.sectLvl)

                            for i in range(2):
                                await self.bot.send_message(message.channel, "***" + str(sectList[xpCheck]) + " Sect has leveled up!*** :cake: :cake: :cake:")

            except Exception as e:
                print("{}".format(e))

    async def second_timer(self):  # tracking xp per second
        secondChecker = 0
        while True:
            global a
            a = datetime.datetime.now()

            for timeCheck in self.xpban:
                if a.second in timeCheck:
                    del self.xpban[0]

            if a.second == 0:
                secondChecker += 1
                print(secondChecker, "/1")
                if secondChecker == 1:
                    upload_file("levels.csv", "/levels.csv")
                    upload_file("sectLevels.csv", "/sectLevels.csv")
            await asyncio.sleep(1)

    async def on_ready(self):
        self.bot.loop.create_task(self.second_timer())


def setup(bot):
    bot.add_cog(XP(bot))
