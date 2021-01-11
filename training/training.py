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
    async def online(self, ctx):
        """Host a training."""
        config = await self.db.find_one({"_id": "config"})
        training_channel = config["training_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(training_channel))
        
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        
        embed = discord.Embed(description=f"{ctx.author.mention}\n\n**__Status__**\n**Online** <:online:797692836911906816>", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.color = self.bot.main_color

        msggg = await setchannel.send(training_mention, embed=embed)
        asyncio.sleep(5)
        await msggg.edit(content=f"{training_mention} | MessageID: {msggg.id}", embed=embed)
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-41 <:online:797692836911906816>")
            
    @commands.command(aliases=["et"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def offline(self, ctx, *, msgID: str):
        """End a training."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed2=discord.Embed(description=f"{ctx.author.mention}\n\n**__Status__**\n**Offline** <:dnd:797692836745183232>", color=0xFF0000)
        await message.edit(embed=embed2, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-42 <:dnd:797692836745183232>")
        await asyncio.sleep(60)
        await message.delete()
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def tenseven(self, ctx, *, msgID: str):
        """break for staff."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed3=discord.Embed(description=f"{ctx.author.mention}\n\n**__Status__**\n**Break (10-7)** <:idle:797695058207178753>", color=0xFFFF00)
        await message.edit(embed=embed3) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>")
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def teneight(self, ctx, *, msgID: str):
        """back for staff."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed4=discord.Embed(description=f"{ctx.author.mention}\n\n**__Status__**\n**Back (10-8)** <:streaming:798080684778061835>", color=0x009dff)
        await message.edit(embed=embed4) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting back 10-8 <:streaming:798080684778061835><:online:797692836911906816>")


            
def setup(bot):
    bot.add_cog(Training(bot))
