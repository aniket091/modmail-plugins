import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class staff(commands.Cog): 
    """An easy way to message staff's status."""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
    
    @commands.command()
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
            
    @commands.command(aliases=["tnew"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def embednew(self, ctx):
        """make a new status message."""
        config = await self.db.find_one({"_id": "config"})
        training_channel = config["training_channel"]
        setchannel = discord.utils.get(ctx.guild.channels, id=int(training_channel))
        
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        
        embed = discord.Embed(description=f"{ctx.author.mention}\n**__Status__**\n**Online** <:online:797692836911906816>", timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.color = self.bot.main_color

        msggg = await setchannel.send(training_mention, embed=embed)
        asyncio.sleep(5)
        await msggg.edit(content=f"{training_mention} | MessageID: {msggg.id}", embed=embed)
        await ctx.message.delete()
        await ctx.send(f"<:yes:793742648141545482> you have created a new status message")
            
    @commands.command(aliases=["n"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def online(self, ctx, *, msgID: str):
        """Online Command"""
        if msgID == None:
            return await ctx.send_help(ctx.command)
            await asyncio.sleep(5)
            await message.delete() 
        
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
            await asyncio.sleep(10)
            await message.delete()
        embed2=discord.Embed(description=f"**__Status__**\n**Online** <:online:797692836911906816>", color=0x00e600, timestamp=datetime.datetime.utcnow())
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed2, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"> {ctx.author.mention}, reporting 10-41 <:online:797692836911906816>")
        
    @commands.command(aliases=["f"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def offline(self, ctx, *, msgID: str):
        """Offline Command"""
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
        embed3=discord.Embed(description=f"**__Status__**\n**Offline** <:dnd:797692836745183232>", color=0xfa1313, timestamp=datetime.datetime.utcnow())
        embed3.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed7=discord.Embed(description=f"**__Status__**\n**Offline** <:invisible:798080684991971348>", color=0xa9a9a9, timestamp=datetime.datetime.utcnow())
        embed7.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed3, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"> {ctx.author.mention}, reporting 10-42 <:dnd:797692836745183232>")
        await asyncio.sleep(100)
        await message.edit(embed=embed7, content=training_mention)
        
    @commands.command(aliases=["10-7"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tenseven(self, ctx, *, msgID: str):
        """10-7 Command"""
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
        await ctx.send(f"> {ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>")
        
    @commands.command(aliases=["10-8"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def teneight(self, ctx, *, msgID: str):
        """10-8 Command"""
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
        embed5=discord.Embed(description=f"**__Status__**\n**Back (10-8)** <:streaming:798080684778061835>", color=0x9900cc, timestamp=datetime.datetime.utcnow())
        embed5.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed6=discord.Embed(description=f"**__Status__**\n**Online** <:online:797692836911906816>", color=0x00ff00, timestamp=datetime.datetime.utcnow())
        embed6.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed5, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"> {ctx.author.mention}, reporting 10-8 <:streaming:798080684778061835>")
        await asyncio.sleep(100)
        await message.edit(embed=embed6, content=training_mention)
        
    @commands.command()
    async def message(self, ctx):
        """message id's of staff"""
        embed7=discord.Embed(title="Staff message id's", description=f"**Aniket  __msgid __: `798418282951999518`\nBlackstorm  __msgid __: `798418289218945064`\nThakur  __msgid__: `798418293690073088`\nGorav  __msgid__: `798418297208045598`\nOmkar  __msgid__ : `798418300143927316`\nHarshak  __msgid__: `798418304523436032`\nPrem Bharti  __msgid__: `798418306394357792`\nRishabh __msgid__: `798418309522784266`\nBhargav  __msgid__: `798418312215527454`\nSourish  __msgid__: `798418314921377812`\nJagbir  __msgid__: `798418326438019132`\nDevuu  __msgid__: `798418327952556093`**", color=0x00ffff, timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)
        await asyncio.sleep(10)
        await message.delete()

        
def setup(bot):
    bot.add_cog(staff(bot))
