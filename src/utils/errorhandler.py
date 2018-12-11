import discord
from discord.ext import commands


class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, error: Exception, ctx: commands.Context):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            await self.bot.send_message(ctx.message.channel, content='**{}s cooldown**'.format(math.floor(error.retry_after)))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
