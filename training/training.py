import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class training(commands.Cog): 
    """second commands for the staff plugin"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.OWNER)
    async def changechannel(self, ctx, channel: discord.TextChannel):
        """Set the training channel!"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"training_channel": channel.id}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the training channel to {channel.mention}", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["offline"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def changeone(self, ctx, *, msgID: str):
        """gone invisible command"""
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
        embed3=discord.Embed(description=f"**__Status__**\n**Offline** <:invisible:798080684991971348>", color=0x009dff, timestamp=datetime.datetime.utcnow())
        embed3.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await asyncio.sleep(5)
        await message.edit(embed=embed3, content=training_mention) # <@&695243187043696650>
        
    @commands.command()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def changetwo(self, ctx, *, msgID: str):
        """back online command two"""
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
        embed4=discord.Embed(description=f"**__Status__**\n**Online** <:online:797692836911906816>", color=0x00ff00, timestamp=datetime.datetime.utcnow())
        embed4.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await asyncio.sleep(5)
        await message.edit(embed=embed4, content=training_mention) # <@&695243187043696650>
        
             
def setup(bot):
    bot.add_cog(training(bot))
