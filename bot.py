# -*- coding: utf-8 -*-

import discord,asyncio,time,csv,random,datetime,os,dropbox
from discord.ext import commands
from discord.ext.commands import Bot
#####REQUIRED
bot = commands.Bot(command_prefix=".!") #bot prefix

xpban=[[""] * 2 for i in range(1)] # create a list for xp timer

sectName, sectSearch, sectOwner, sectTag, sectLvl, sectXP = list(),list(),list(),list(),list(),list()     #create 6 lists

requiredXP = [ 5000,7000,8000,10000,15000, #1-4
                   20000,25000,30000,35000, #5-8.. etc
                   400000,45000,50000,55000] #required xp for the next level
    
def download_file(file_to,file_from):
    dbx = dropbox.Dropbox(os.environ['DROPBOX_TOKEN'])
    f = open(file_to,"w")                    
    metadata,res = dbx.files_download(file_from)
    f.write(str(res.content)[2:-1])
    f.close()
    
def upload_file(file_from, file_to):
    dbx = dropbox.Dropbox(os.environ['DROPBOX_TOKEN']) #DROXBOX_TOKEN
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode.overwrite)
    f.close()

    
download_file("sects.csv","/sects.csv") #download file from dbx if run or reset

##open sects.csv file
with open("sects.csv", "r+", encoding='utf-8') as sectfile:    #Grab it all from the file
    reader = csv.reader(sectfile)
    for row in reader:    #run through each row
                namesplit = row[0].split("[")
                sectName.append(namesplit[0]),sectSearch.append(namesplit[1][:-1])
                
                sectOwner.append(row[1]), sectTag.append(row[2])
                sectLvl.append(int(row[3])), sectXP.append(int(row[4]))
    sectfile.close()    #close file


async def second_timer(): ##will be our xp timer
    secondChecker = 0 #set checker to 0 this is going to count up every minute
    while True: #infinite
        global a
        a = datetime.datetime.now()
        
        for timeCheck in xpban:
            if a.second in timeCheck:
                del xpban[0]

        if a.second == 0: #starting from 0 seconds
            secondChecker +=1 #add 1 each time a minute passes
            if secondChecker == 3: #if 3 minutes have passed
                secondChecker = 0 #set checker to 0
                upload_file("sects.csv","/sects.csv") #upload file to dbx
                
        await asyncio.sleep(1) #asyncio.sleep allows it to run in the background without making the program stop for that period of time its a second counter
        
##when bot loads
@bot.event  
async def on_ready():   #print On and change status once running 
    print("On")
    await bot.change_presence(game=discord.Game(name="Testing saves and stuff"))
    bot.loop.create_task(second_timer())


@bot.command(pass_context=True)
async def sects(ctx, arg="a", arg2=0):
    sectNumber = len(sectName) # how many sects there are
    argCh = "na" #create a variable
    argSet = False #Check
    
    for sects in sectSearch: #check if arg in sects
        if arg.lower() == sects.lower(): #make sure both compared are lowercase
            argCh = sectSearch.index(sects) #set argCh to the index

            #discord bot embed and speech
            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name=str(sectName[argCh]))
            embed.add_field(name="Leader", value=str(sectOwner[argCh]))
            embed.add_field(name="XP until Next level", value= str(requiredXP[sectLvl[argCh]] - sectXP[argCh])+"xp ("+str(requiredXP[sectLvl[argCh]])+")")
            embed.add_field(name="Level", value=str(sectLvl[argCh]+1))
            
            await bot.say(embed=embed,delete_after=10)
            break

    
    if arg.lower() in ["h","help"] and argCh == "na": #display help
        embed=discord.Embed(description="```Usages:\n.!sects <search tag> - display tagged sect\n\nSearch tags available:\n"+str(sectSearch)+"\n\n.!sects a - display all sects\n.!sects lb - display sect leaderboards```",color=0x31c7ce)
        await bot.say(embed=embed, delete_after=20)

        
    elif arg.lower() == "a" and argCh == "na": #display all

            rewritecsv = open('sects2.csv', 'w', encoding='utf-8')
            for allSects in range(sectNumber):
                rewritecsv.write(sectName[allSects]+"["+sectSearch[allSects]+"],"+sectOwner[allSects]+","+sectTag[allSects]+", "+str(sectLvl[allSects])+", "+str(sectXP[allSects])+"\n")
            rewritecsv.close()

            tempName = list(sectName)
            tempOwner = list(sectOwner)
            tempLvl = list(sectLvl)
            tempXP = list(sectXP)
            tempXPC = list(sectXP)

            for xptotal in range(sectNumber):
                for getxp in range(sectLvl[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]
            tempXP, tempName, tempOwner,tempLvl, tempXPC = zip(*sorted(zip(tempXP, tempName, tempOwner,tempLvl, tempXPC),reverse=True))

            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Sects")

            if arg2 != 0:
               arg2 -=1
               

                
            for printOut in range(0+ (3 * arg2 ), 3+ ( 3 * arg2 )):

                try:
                    embed.add_field(name=str(tempName[printOut]), value="Lead by "+ tempOwner[printOut],inline=False)
                    embed.add_field(name="Level", value=str(tempLvl[printOut]+1))
                    embed.add_field(name="XP until Next level", value= str(requiredXP[tempLvl[printOut]] - tempXPC[printOut])+"xp ("+str(requiredXP[tempLvl[printOut]])+")")
                except IndexError:
                    break
                
                if printOut != 3+(3*arg2)-1:
                    embed.add_field(name="\u200b", value="\u200b",inline=False)
            embed.add_field(name="Notes", value="I recommend you to start using < .!sect lb > as this is WIP! \n< .!sect a > now has pages and will eventually display descriptions! If you want to continue using < .!sect a > it is now < .! sect a [page] >",inline=False)
                
            await bot.say(embed=embed,delete_after=25)

            
    elif arg.lower() == "lb" and argCh == "na" : #display leaderboard
            tempName = list(sectName) 
            tempXP = list(sectXP)
            tempXPC = list(sectXP)
            tempLvl = list(sectLvl)
            
            for xptotal in range(sectNumber):
                for getxp in range(sectLvl[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]

            tempXP, tempName, tempXPC, tempLvl = zip(*sorted(zip(tempXP,tempName,tempXPC,tempLvl),reverse=True))
            
            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Leaderboard")

            for i in range(len(tempName)):
                if i != len(tempName):
                    embed.add_field(name="#"+str(i+1)+" "+tempName[i], value=str(tempXPC[i])+" / "+str(requiredXP[tempLvl[i]-1])+" ("+str(tempXP[i])+")", inline=False)
            await bot.say(embed=embed,delete_after=20)

@bot.event
async def on_message(message):
    sectNumber = len(sectName)
    if message.channel.id == "326959934187110402":
        pass
    else:
        try:
            global xpban,a
            located = False

            search = message.author.id
            for idCheck in xpban:
                if search in idCheck:
                    located = True
            if message.author.nick is None or located == True:
                pass

            else:    
                xpban +=[[""] * 2 for i in range(1)]
                xpban[len(xpban)-2][0] = (message.author.id)
                xpban[len(xpban)-2][1] = (a.second)


                for findTag in range(sectNumber):
                    if sectTag[findTag].upper() in message.author.nick.upper() :                    
                                sectXP[findTag] += random.randint(2,5)    #set xp
                                print(str(sectName[findTag])+" = "+str(sectXP[findTag])+"xp")

                for xpCheck in range(sectNumber):
                    if sectXP[xpCheck] >= requiredXP[sectLvl[xpCheck]]:
                        sectXP[xpCheck] = 0
                        sectLvl[xpCheck] +=1
                        await bot.send_message(message.channel,"***"+str(sectName[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                        await bot.send_message(message.channel,"***"+str(sectName[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")

            rewritecsv = open('sects.csv', 'w', encoding='utf-8')
            for allSects in range(sectNumber):
                rewritecsv.write(sectName[allSects]+"["+sectSearch[allSects]+"],"+sectOwner[allSects]+","+sectTag[allSects]+", "+str(sectLvl[allSects])+", "+str(sectXP[allSects])+"\n")
            rewritecsv.close()
        except:
            pass

    await bot.process_commands(message)


bot.run(os.environ['BOT_TOKEN'])
  #Made by Weiqing#2360 & Perpetual Phoenix#0363
