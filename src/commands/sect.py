import discord
from discord.ext import commands
from src.data.sectInfo import *
from src import config


class Sect:
    def __init__(self, bot):
        self.bot = bot
        self.sectLvl = config.sectLvl
        self.sectXP = config.sectXP

    @commands.command(pass_context=True)
    async def invite(self, ctx, user: discord.User):

        inviteMsg = f"Hey {user.mention}! {ctx.message.author.mention} has invited you to join their sect. \n\n**Status: Pending**"
        msg = await self.bot.send_message(ctx.message.channel,
                                          inviteMsg)

        reactions = ['✅', '❌']
        for reaction in reactions:
            await self.bot.add_reaction(msg, reaction)

        try:
            reaction, reactor = await self.bot.wait_for_reaction(['✅', '❌'], user=user, timeout=600, message=msg)

            if reaction.emoji == "✅":
                reply = "Accepted"
                for i in range(len(sectTags)):
                    if sectTags[i] in ctx.message.author.display_name:
                        try:
                            if sectTags[i] == "Lord" or sectTags[i] == "⧹Cult⧸":
                                await self.bot.change_nickname(user, sectTags[i] + " " + user.name)
                            else:
                                await self.bot.change_nickname(user, user.name + " " + sectTags[i])
                            break
                        except Exception as caughtError:
                            await self.bot.send_message(ctx.message.channel, "An error has occured,\n",caughtError,"\nPlease ping a mod")

            elif reaction.emoji == "❌":
                reply = "Rejected"

        except TypeError:
            reply = "Timed Out"

        await self.bot.edit_message(msg, new_content=inviteMsg.replace("Pending", reply))
        await self.bot.send_message(ctx.message.author, f"{user} has {reply.lower()} your sect invite.")
        await self.bot.send_message(self.bot.get_channel("477777298431672321"), f"{ctx.message.author} has invited {user} to their sect. | {reply}")
        await self.bot.clear_reactions(msg)

    @commands.command(pass_context=True)
    async def sects(self, ctx, arg="lb"):
        if arg.lower() not in ["l", "lb", "h", "help", "a", "hof"]:
            for sects in sectCall:  # check if arg in sects
                if arg.lower() == sects.lower():  # make sure both compared are lowercase
                    argCh = sectCall.index(sects)  # set argCh to the index
                    embed = discord.Embed(color=0x71cecb)
                    embed.set_author(name=str(sectList[argCh]))
                    embed.add_field(
                        name="Leader", value=str(sectOwner[argCh]))
                    embed.add_field(name="XP until Next level", value=str(
                        requiredXP[self.sectLvl[argCh]] - self.sectXP[argCh]) + "xp (" + str(requiredXP[self.sectLvl[argCh]]) + ")")
                    embed.add_field(
                        name="Level", value=str(self.sectLvl[argCh] + 1))
                    embed.add_field(name="Description",
                                    value=str(sectDescription[argCh]))

                    await self.bot.say(embed=embed, delete_after=25)
                    break

        if arg.lower() in ["h", "help"]:
            embed = discord.Embed(color=3447003)
            embed.set_author(name="Usage")
            embed.add_field(name="<.sects a>", value="Redundant")
            embed.add_field(
                name="<.sects lb>", value="Display the sect leaderboard", inline=False)
            embed.add_field(name="<.sects hof>",
                            value="Display the hall of fame", inline=False)
            embed.add_field(
                name="<.sects [search tag] >", value="Display tagged sects\n\u200b", inline=False)
            embed.add_field(name="Search Tags",
                            value=sectCall, inline=False)

            await self.bot.say(embed=embed, delete_after=20)

        elif arg == "a":
            embed = discord.Embed(color=0xabcdef)
            embed.set_author(name="Sects Info!")
            embed.add_field(name="This command is no longer in use! Instead use <.!sects lb> or just <.!sects now!>",
                            value="This change has been due to the fact as sects have grown, the command takes up the entire screen in #bot_commands. This is too much!", inline=False)
            await self.bot.say(embed=embed, delete_after=25)

        elif arg in ["l", "lb"]:
            tempName = list(sectList)
            tempTag = list(sectCall)
            tempXPC = list(self.sectXP)
            tempXP = list(self.sectXP)
            tempLvl = list(self.sectLvl)
            tempDesc = list(sectDescription)

            for xptotal in range(len(self.sectXP)):
                for getxp in range(self.sectLvl[xptotal]):
                    tempXP[xptotal] += requiredXP[getxp]

            tempXP, tempName, tempXPC, tempLvl, tempTag, tempDesc = zip(
                *sorted(zip(tempXP, tempName, tempXPC, tempLvl, tempTag, tempDesc), reverse=True))     

            embed = discord.Embed(color=0x896fc4)
            embed.set_author(name="Leaderboard")

            for i in range(len(tempName)):
                embed.add_field(name="#" + str(i + 1) + " " + tempName[i] + " [" + tempTag[i] + "]", value=str(
                    tempXPC[i]) + " / " + str(requiredXP[tempLvl[i]]) + " (" + str(tempXP[i]) + ")", inline=False)

            await self.bot.say(embed=embed, delete_after=20)


def setup(bot):
    bot.add_cog(Sect(bot))
