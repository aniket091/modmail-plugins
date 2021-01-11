import discord
from discord.ext import commands
import asyncio

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        await ctx.message.delete()
        message = await ctx.send(f"{ctx.author.mention}, reporting 10-41 <:online:797692836911906816>") 
        
    
    @commands.command()
    async def offline(self, ctx):
        await ctx.message.delete()
        await message.edit(content="reporting 10-7 <:idle:797695058207178753>")
        
        
    @commands.command()
    async def tenseven(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>") 
        
        
    @commands.command()
    async def teneight(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-8 <:online:797692836911906816>") 
                
        
def setup(bot):
    bot.add_cog(staff(bot))
