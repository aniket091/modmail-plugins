import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def log(self, ctx, *, message=None):
        """Make the bot say something"""
        await ctx.message.delete()
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Say(bot))
