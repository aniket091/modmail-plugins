import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class staff2(commands.Cog): 
    """An easy way for HR's to manage training announcements."""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
                    
    @commands.command(aliases=["f"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def offline(self, ctx, *, msgID: str):
        """offline for staff2."""
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
        embed3=discord.Embed(description=f"**__Status__**\n**Offline** <:dnd:797692836745183232>", color=0xFF0000, timestamp=datetime.datetime.utcnow())
        embed3.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        asyncio.sleep(5)
        await message.edit(embed=embed6, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        
    @commands.command(aliases=["10-7"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tensevenvghbjhvbgh(self, ctx, *, msgID: str):
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
        embed4=discord.Embed(description=f"**__Status__**\n**Break (10-7)** <:idle:797695058207178753>", color=0xffff00, timestamp=datetime.datetime.utcnow())
        embed4.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed4, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>")
        
    @commands.command(aliases=["10-8"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def teneight(self, ctx, *, msgID: str):
        """back for staff2."""
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
        embed5=discord.Embed(description=f"**__Status__**\n**Online** <:online:797692836911906816>", color=0x009dff, timestamp=datetime.datetime.utcnow())
        embed5.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        asyncio.sleep(5)
        await message.edit(embed=embed5, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tennightsad(self, ctx, *, msgID: str):
        """godnight for staff."""
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
        embed6=discord.Embed(description=f"**__Status__**\n**Offline** <:invisible:798080684991971348>", color=0x009dff, timestamp=datetime.datetime.utcnow())
        embed6.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed6, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting bye bye <:invisible:798080684991971348>")


            
def setup(bot):
    bot.add_cog(staff2(bot))
