import discord
from discord.ext import commands
import asyncio

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def online(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-41 <:online:797692836911906816>") 
        
    
    @commands.command()
    async def offline(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-42 <:dnd:797692836745183232>")  
        
        
    @commands.command()
    async def break(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>") 
        
        
def setup(bot):
    bot.add_cog(staff(bot))
