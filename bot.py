import discord,asyncio,time,csv,random,datetime,os
from discord.ext import commands
from discord.ext.commands import Bot

xpban=[[""] * 2 for i in range(1)]

sectList = ["Autarch Flipping","Explosion","Blank"]              #ADD NEW SECTS HERE
sectTags = ["「 ELON 」","Explosion","『　　』"]                  #ADD NEW TAGS HERE
sectOwner = ["Perpetual Phoenix#0363", "Megumin_Explosion#9614", "Storm#6666"]

sectXP = list() #create empty xp list                                       When creating a new sect, make sure to add ", 0" to the end of level.csv. Same with sectLevels
trueSectLevel = list() #create empty level list                               This will allow it to start tracking xp for that sect without errors
requiredXP = [5000,7000,8000,10000,15000,20000,25000,30000,35000,400000,45000,50000,55000]

with open("levels.csv", "r+") as sectLevels:        #Grab all XP levels from levels.csv due to startup/restart
    reader = csv.reader(sectLevels)
    for row in reader:
        for i in range(len(row)):
            sectXP.append(int(row[i]))
    sectLevels.close()

with open("sectLevels.csv", "r+") as trueLevel:        #Grab all true levels from sectLevels.csv due to startup/restart
    reader = csv.reader(trueLevel)
    for row in reader:
        for i in range(len(row)):
            trueSectLevel.append(int(row[i]))
    trueLevel.close()

async def second_timer(): ##will be our xp timer
    while True:
        global a
        a = datetime.datetime.now()
        
        for timeCheck in xpban:
            if a.second in timeCheck:
                del xpban[0]
                
        await asyncio.sleep(1)
 
bot = commands.Bot(command_prefix=".!") #bot prefix
#
@bot.event  
async def on_ready():   #when bot is ready will print on a new line, and change bot playing status
    
    print("_____________________\nSect XP Tracking On")
    await bot.change_presence(game=discord.Game(name="Tracking Sect XP"))
    bot.loop.create_task(second_timer())
#
@bot.command(pass_context=True)

async def sects(ctx):
    for printOut in range(len(sectList)):
        embed=discord.Embed(color=0xabcdef)
        embed.set_author(name=str(sectList[printOut]))
        embed.add_field(name="Leader", value=str(sectOwner[printOut]))
        embed.add_field(name="Level", value=str(trueSectLevel[printOut]+1))
        embed.add_field(name="XP until Next level", value= str(requiredXP[trueSectLevel[printOut]] - sectXP[printOut])+"xp ("+str(requiredXP[trueSectLevel[printOut]])+")")
        await bot.send_message(ctx.message.server.get_member(ctx.message.author.id), embed=embed) 
#      
@bot.event
async def on_message(message):
    try:
        global xpban,a
        located = False

        search = message.author.id
        for idCheck in xpban:
            if search in idCheck:
                located = True

        if ".!sects" in message.content:
            pass
        
        elif message.author.nick is None or located == True:
            pass
        
        else:    
            xpban +=[[""] * 2 for i in range(1)]
            xpban[len(xpban)-2][0] = (message.author.id)
            xpban[len(xpban)-2][1] = (a.second)

            
            for findTag in range(len(sectTags)):
                if sectTags[findTag].upper() in message.author.nick.upper() :                    
                            sectXP[findTag] += random.randint(2,5)    #set xp
                            print(str(sectList[findTag])+" = "+str(sectXP[findTag])+"xp")
                            
            for xpCheck in range(len(sectList)):
                if sectXP[xpCheck] >= requiredXP[trueSectLevel[xpCheck]]:
                    sectXP[xpCheck] = 0
                    trueSectLevel[xpCheck] +=1
                    await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                    await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                    
            lev = open('sectLevels.csv', 'w')
            xplev = open('levels.csv', 'w')
            for allSects in range(len(sectList)):
                lev.write(str(trueSectLevel[allSects]))
                xplev.write(str(sectXP[allSects]))
                if allSects != len(sectList)-1:
                    lev.write(",")
                    xplev.write(",")
            lev.close()
            xplev.close()

        await bot.process_commands(message)
    except:
        pass
bot.run(os.environ['BOT_TOKEN'])
#Made by Weiqing#2360 & Perpetual Phoenix#0363
