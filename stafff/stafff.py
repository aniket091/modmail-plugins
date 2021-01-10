import discord
from discord.ext import commands
import asyncio

class stafff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        message = await ctx.send('testing')
        await asyncio.sleep(0.3)
        await message.edit(content='v2')

        
def setup(bot):
    bot.add_cog(stafff(bot))
