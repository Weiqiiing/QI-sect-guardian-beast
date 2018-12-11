import discord
from discord.ext import commands


class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def millie(self):
        image = "https://i.imgur.com/rB2Kg6X.png"
        embed = discord.Embed()
        embed.set_image(url=image)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
