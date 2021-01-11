import discord
from discord.ext import commands
import asyncio

class stafff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(ctx):
      message = await ctx.send("hello")
      await asyncio.sleep(1)
      await message.edit(content="newcontent")
   
        
def setup(bot):
    bot.add_cog(stafff(bot))
