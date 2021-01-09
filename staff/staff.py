import discord
from discord.ext import commands

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
@commands.command()
async def online(self, ctx, member : discord.Member):
    await ctx.send(f"{member} reporting 10-41")
        
              
def setup(bot):
    bot.add_cog(staff(bot))
