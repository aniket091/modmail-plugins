import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def say(self, ctx, *, message):
        """Make the bot say something"""
        await ctx.message.delete()
        await ctx.send(message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere"))

def setup(bot):
    bot.add_cog(Say(bot))
