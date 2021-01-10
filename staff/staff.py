import discord
from discord.ext import commands

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        await ctx.send(f"{ctx.author.mention}, reporting online(10-41) <:online:797692836911906816>")
        
        
def setup(bot):
    bot.add_cog(staff(bot))
