import discord
from discord.ext import commands

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        await ctx.send("{message.author.mention}")
        
        
def setup(bot):
    bot.add_cog(staff(bot))
