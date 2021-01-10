import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Shift(commands.Cog): 
    """An easy way for HR's to manage shift announcements."""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
    
    @commands.command(aliases=["schannel"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def shiftchannel(self, ctx, channel: discord.TextChannel):
        """Set the shift channel!"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"shift_channel": channel.id}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the shift channel to {channel.mention}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(aliases=["smention"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def shiftmention(self, ctx, *, mention: str):
        """Sets the shift mention"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"shift_mention": mention}}, upsert=True)
        
        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Changed Mention", value=f"Successfully changed the shift mention to {mention}", inline=False)
        
        await ctx.send(embed=embed)
            
    @commands.command(aliases=["s"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def shift(self, ctx):
        """Host a shift."""
        config = await self.db.find_one({"_id": "config"})
        shift_channel = config["shift_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(shift_channel))
        
        try:
            shift_mention = config["shift_mention"]
        except KeyError:
            shift_mention = ""
        
        embed = discord.Embed(description="{ctx.author.mention} <:online:797692836911906816>", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.color = self.bot.main_color
   
        msggg = await setchannel.send(shift_mention, embed=embed)
        asyncio.sleep(5)
        await msggg.edit(content=f"{shift_mention} | msgID: {msggg.id}", embed=embed)
        await ctx.send("<a:check:742680789262663710> | Shift announcement has been posted!")
            
    @commands.command(aliases=["es"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def endshift(self, ctx, *, msgID: str):
        """End a shift."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["shift_channel"])
        try:
            shift_mention = config["shift_mention"]
        except KeyError:
            shift_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the shift channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed2=discord.Embed(description=f"{ctx.author.mention} <:dnd:797692836745183232>", color=0xe74c3c)
        await message.edit(embed=embed2) # <@&695243187043696650>
        await ctx.send("<a:check:742680789262663710> | Shift announcement has been edited and the shift has ended!")
        await asyncio.sleep(600)
        await message.delete()
            
def setup(bot):
    bot.add_cog(Shift(bot))
