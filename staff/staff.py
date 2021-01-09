import discord
from discord.ext import commands, tasks
import asyncio

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
@commands.command()
async def ping(self, ctx, member : discord.Member):
    await ctx.message.delete()
    await ctx.send(f"an{member} reporting 10-41 an")
        
              
def setup(bot):
    bot.add_cog(staff(bot))
