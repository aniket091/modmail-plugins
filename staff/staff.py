import discord
from discord.ext import commands

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{0.author.mention} reporting 10-41")
        
        
def setup(bot):
    bot.add_cog(staff(bot))
