import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Training(commands.Cog): 
    """An easy way for HR's to manage training announcements."""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
    
    @commands.command(aliases=["tchannel"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def trainingchannel(self, ctx, channel: discord.TextChannel):
        """Set the training channel!"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"training_channel": channel.id}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the training channel to {channel.mention}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(aliases=["tmention"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def trainingmention(self, ctx, *, mention: str):
        """Sets the training mention"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"training_mention": mention}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Changed Mention", value=f"Successfully changed the training mention to {mention}", inline=False)
        
        await ctx.send(embed=embed)
            
    @commands.command(aliases=["train"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def training(self, ctx):
        """Host a training."""
        config = await self.db.find_one({"_id": "config"})
        training_channel = config["training_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(training_channel))
        
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        
        embed = discord.Embed(description=f"{ctx.author.mention} <:online:797692836911906816>", timestamp=datetime.datetime.utcnow())
        embed.color = self.bot.main_color

        msggg = await setchannel.send(training_mention, embed=embed)
        asyncio.sleep(5)
        await msggg.edit(content=f"{training_mention} | msgID: {msggg.id}", embed=embed)
            
    @commands.command(aliases=["et"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def endtraining(self, ctx):
        """End a training."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        message = {msggg.id}
        embed2=discord.Embed(description=f"{ctx.author.mention} <:dnd:797692836745183232>", color=0xe74c3c)
        embed2.color = self.bot.main_color
        await message.edit(embed=embed2, content=training_mention) # <@&695243187043696650>
        
        await ctx.send("<a:check:742680789262663710> | Training announcement has been edited and the training has ended!")
        await asyncio.sleep(5)
        await message.delete()
            
def setup(bot):
    bot.add_cog(Training(bot))
