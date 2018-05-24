# -*- coding: utf-8 -*-
import discord,asyncio,time,csv,random,datetime,os,dropbox
from discord.ext import commands
from discord.ext.commands import Bot

xpban=[[""] * 2 for i in range(1)]

sectList = ["Autarch Flipping", "Explosion","Blank","Thousand and One Petals","Debauchery Tea Party","Sort Post A Massege"] #Name of Sect
sectCall = ["ELON","Exp","Blank","PETALS","TeaParty","spam"] #call for .!sect <name>
sectTags = ["「 ELON 」","Explosion","『　　』","《 PETALS 》","[TeaParty]","[spam]"] #Tag required for xp   
sectOwner = ["Perpetual Phoenix", "Megumin_Explosion", "Storm","Ziyun","ZaChan","Leechie_SPLOSION"] #Owner of Sect
sectDescription = ["ummm..\nsoon",  #Elon
                    "EXPlOSION that's all\nFounded by megumin", #Explosion
                    "Allowing knowledge to flow freely to one another, while not pondering over futile matters laying in conflict with the state of mind.\nBlank is the way your soul has to feel for proper understanding and mental fortitude.", #Blank
                    "NA", #Petals
                    "NA", #Tea Party
                    "NA", #Spam
                   ]
					
sectXP = list() #create empty xp list
sectLvl = list() #create empty level list 

requiredXP = [ 5000,7000,8000,10000,15000,20000,25000,30000,35000,400000,45000,50000,55000] #xp required for next level

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

def openFile(fileName, openIn,listAdd):
        with open(fileName, openIn) as fData:
            reader = csv.reader(fData)
            for row in reader:
                for i in range(len(row)):
                    listAdd.append(int(row[i]))
        fData.close()
        
def writeFile(fileName, openIn,listWrite):
        fData = open(fileName, openIn)
        for allSects in range(len(sectCall)):
            fData.write(str(listWrite[allSects]))
            if allSects != len(sectCall)-1:
                fData.write(",")
        fData.close()
        
download_file("levels.csv","/levels.csv")
download_file("sectLevels.csv","/sectLevels.csv")
        
openFile("levels.csv", "r+",sectXP)
openFile("sectLevels.csv", "r+",sectLvl)

async def second_timer(): ##will be our xp timer
    secondChecker = 0
    while True:
        global a
        a = datetime.datetime.now()
        
        for timeCheck in xpban:
            if a.second in timeCheck:
                del xpban[0]

        if a.second == 0:
            secondChecker +=1
            print(secondChecker,"/1")
            if secondChecker == 1:
                secondChecker = 0
                
                upload_file("levels.csv","/levels.csv")
                upload_file("sectLevels.csv","/sectLevels.csv")
                               
        await asyncio.sleep(1)


bot = commands.Bot(command_prefix=".!") #bot prefix
	

@bot.event  
async def on_ready():   #when bot is ready will print on a new line, and change bot playing status
    
    print("_____________________\nSect XP Tracking On")
    await bot.change_presence(game=discord.Game(name="Sect Tracting. V3"))
    bot.loop.create_task(second_timer())

@bot.command(pass_context=True)
async def sects(ctx, arg="lb"):
    
    if arg.lower() not in ["l","lb","h","help","a","hof"]:
        for sects in sectCall: #check if arg in sects
                if arg.lower() == sects.lower(): #make sure both compared are lowercase
                        argCh = sectCall.index(sects) #set argCh to the index
                        embed=discord.Embed(color=0x71cecb)
                        embed.set_author(name=str(sectList[argCh]))
                        embed.add_field(name="Leader", value=str(sectOwner[argCh]))
                        embed.add_field(name="XP until Next level", value= str(requiredXP[sectLvl[argCh]] - sectXP[argCh])+"xp ("+str(requiredXP[sectLvl[argCh]])+")")
                        embed.add_field(name="Level", value=str(sectLvl[argCh]+1))
                        embed.add_field(name="Description", value=str(sectDescription[argCh]))
                        
                        
                        await bot.say(embed=embed,delete_after=10)
                        break

    if arg.lower() in ["h","help"]:
        embed=discord.Embed(color=3447003)
        embed.set_author(name="Usage")
        embed.add_field(name="<.!sects a>", value="Redundant")
        embed.add_field(name="<.!sects lb>", value="Display the sect leaderboard",inline=False)
        embed.add_field(name="<.!sects hof>", value="Display the hall of fame",inline=False)
        embed.add_field(name="<.!sects [search tag] >", value="Display tagged sects\n\u200b",inline=False)
        embed.add_field(name="Search Tags",value=sectCall,inline=False)
        

        await bot.say(embed=embed, delete_after=20)

        
    elif arg == "a":
            embed=discord.Embed(color=0xabcdef)
            embed.set_author(name="Sects Info!")
            embed.add_field(name="This command is no longer in use! Instead use <.!sects lb> or just <.!sects now!>", value="This change has been due to the fact as sects have grown, the command takes up the entire screen in #bot_commands. This is too much!",inline=False)
            await bot.say(embed=embed,delete_after=25)

            
    elif arg in ["l","lb"]:
            tempName = list(sectList) 
            tempTag = list(sectCall)
            tempXPC = list(sectXP)
            tempXP = list(sectXP)
            tempLvl = list(sectLvl)
            tempDesc = list(sectDescription)

            for xptotal in range(len(sectXP)):
                for getxp in range(sectLvl[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]

            tempXP, tempName, tempXPC, tempLvl,tempTag,tempDesc = zip(*sorted(zip(tempXP,tempName,tempXPC,tempLvl,tempTag,tempDesc),reverse=True))
            

            embed=discord.Embed(color=0x896fc4)
            embed.set_author(name="Leaderboard")

            for i in range(len(tempName)):
                    embed.add_field(name="#"+str(i+1)+" "+tempName[i]+" ["+tempTag[i]+"]", value=str(tempXPC[i])+" / "+str(requiredXP[tempLvl[i]])+" ("+str(tempXP[i])+")",inline=False)

            await bot.say(embed=embed,delete_after=20)

    elif arg in ["hof"]: #TBD
            pass

@bot.event
async def on_message(message):
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
    
                
                for findTag in range(len(sectCall)):
                    if sectTags[findTag].upper() in message.author.nick.upper() :                    
                                sectXP[findTag] += random.randint(2,5)    #set xp
                                print(str(sectList[findTag])+" = "+str(sectXP[findTag])+"xp") 
                                writeFile("levels.csv", "w", sectXP)

                                        
                for xpCheck in range(len(sectCall)):
                    if sectXP[xpCheck] >= requiredXP[sectLvl[xpCheck]]:
                        sectXP[xpCheck] = 0
                        sectLvl[xpCheck] +=1
                        writeFile("sectLevels.csv", "w", sectLvl)

                        for i in range(2):
                            await bot.send_message(message.channel,"***"+str(sectList[xpCheck])+" Sect has leveled up!*** :cake: :cake: :cake:")
                
        except:
            pass
    await bot.process_commands(message)
bot.run(os.environ['BOT_TOKEN'])
  #Made by Weiqing#2360 & Perpetual Phoenix#0363
