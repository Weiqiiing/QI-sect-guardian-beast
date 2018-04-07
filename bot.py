import discord,asyncio,time,csv,random,datetime,os
from discord.ext import commands
from discord.ext.commands import Bot


bot = commands.Bot(command_prefix="") #bot prefix
file = open("testfile.txt","r")
f = file.read()
file.close()

async def on_ready():   #when bot is ready will print on a new line, and change bot playing status
    
    print("_____________________\nSect XP Tracking On")
    await bot.change_presence(game=discord.Game(name="Tracking"))

@bot.command(pass_context=True)
async def x(ctx):
        print(f)
        await bot.say("test")
        
bot.run(os.environ['BOT_TOKEN'])
