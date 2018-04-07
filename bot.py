import discord,asyncio,time,csv,random,datetime
from discord.ext import commands
from discord.ext.commands import Bot


bot = commands.Bot(command_prefix="") #bot prefix
file = open("testfile.txt","r")
f = file.read()
file.close()



@bot.command(pass_context=True)
async def x(ctx):
        print(f)
        await bot.say("test")
        
bot.run(os.environ['BOT_TOKEN'])
