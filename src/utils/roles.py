import discord
from discord.ext import commands
import math
from src.data.roleInfo import *


class Roles:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, aliases=["iam"])
	async def addrole(self, ctx, *roleToAdd):
		roleToAdd = " ".join(roleToAdd)
		if roleToAdd.title() in usableRoles or roleToAdd.lower() == "none":
			currentRoles = [x.name for x in ctx.message.author.roles]
			if any(x in currentRoles for x in usableRoles):
				for i in range(len(usableRoles)):
					if usableRoles[i] in currentRoles and usableRoles[i] != "Interested in Events":
						role = discord.utils.get(
							ctx.message.server.roles, name=usableRoles[i])
						await self.bot.remove_roles(ctx.message.server.get_member(ctx.message.author.id), role)
			if roleToAdd.lower() == "none":
				await self.bot.say("Your coloured role has been removed.")
			else:
				await self.bot.say("Adding '" + str(roleToAdd) + "' to " + str(ctx.message.author.name))
				if roleToAdd.lower() == "interested in events":
					role = discord.utils.get(
						ctx.message.server.roles, name="Interested in Events")
				else:
					role = discord.utils.get(
						ctx.message.server.roles, name=roleToAdd.title())

				await self.bot.add_roles(ctx.message.server.get_member(ctx.message.author.id), role)
		else:
			await self.bot.say("That role is not available!")

	@commands.command(pass_context=True)
	async def roles(self, ctx):
		allRoles = ["Literary Snobs", "Polygamist Reader", "Habitual Book Clubber", "Stockpiler", "Re-Reader", "Physical Book Loyalist", "Spoiler Lover", "Nonfiction Lover", "Fiction Fanatics", "Emotional Reader", "Book Juggler", "Die-Hard Reader",
					"Weekend Warrior Reader", "Obsessive Bibliophile", "Tentative Reader", "Shy Reader", "Librocubicularist", "Grumpy Reader", "Book Eater", "Seasonal Reader", "Trend Reader", "Moody Reader", "Practical Reader", "Slow Reader"]
		embed = discord.Embed(
			title=f"**There are {len(allRoles)} self-assignable roles.**", color=16711680)
		pages = {}

		for x in range(math.ceil(len(allRoles) / 15)):
			try:
				pages[f"page{x}"] = " \n".join(allRoles[0:15])
				del allRoles[0:14]
			except Exception:
				pages[f"page{x}"] = " \n".join(allRoles[:len(allRoles) - 1])
				del allRoles[:len(allRoles)]

		embed.add_field(name="**⟪Cultivation Methods⟫**", value=pages["page0"])
		current = 0
		embed.set_footer(text=f"{current+1}/{len(pages)}")
		msg = await self.bot.send_message(ctx.message.channel, embed=embed)

		nav = ["⬅", "➡"]
		for emote in nav:
			await self.bot.add_reaction(msg, emote)

		for x in range(5):

			try:
				reaction, reactor = await self.bot.wait_for_reaction(nav, user=ctx.message.author, timeout=10, message=msg)
				if reaction.emoji == "➡" and current == 0:
					current += 1
				elif reaction.emoji == "⬅" and current == 1:
					current -= 1

				embed.remove_field(0)
				embed.set_footer(text=f"{current+1}/{len(pages)}")
				embed.add_field(name="**⟪Cultivation Methods⟫**",
								value=pages[f"page{current}"])
				await self.bot.edit_message(msg, embed=embed)

			except TypeError:
				await self.bot.clear_reactions(msg)

		await self.bot.clear_reactions(msg)


def setup(bot):
	bot.add_cog(Roles(bot))
