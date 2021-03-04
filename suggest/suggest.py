import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class Suggest(commands.Cog):
    """
    Let's you send a suggestion to a designated channel.
    """

    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

        self.banlist = dict()

        asyncio.create_task(self._set_mod_val())

    async def _update_mod_db(self):
        await self.coll.find_one_and_update(
            {"_id": "mod"}, {"$set": {"banlist": self.banlist,}}, upsert=True,
        )

    async def _set_mod_val(self):
        mod = await self.coll.find_one({"_id": "mod"})

        if mod is None:
            return

        self.banlist = mod["banlist"]

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def suggest(self, ctx, *, suggestion):
        """
        Suggest something!
        **Usage**:
        {prefix}suggest add coffee to bar!
        """
        if str(ctx.author.id) not in self.banlist:
            async with ctx.channel.typing():
                config = await self.coll.find_one({"_id": "config"})
                if config is None:
                    embed = discord.Embed(
                        title="Suggestion channel not set.", color=self.bot.error_colour
                    )
                    embed.set_author(name="Error.")
                    embed.set_footer(text="Task failed successfully.")
                    await ctx.send(embed=embed)
                else:
                    suggestion_channel = self.bot.get_channel(
                        int(config["suggestion-channel"]["channel"])
                    )

                    embed = discord.Embed(
                        color=0xffff00
                    )
                    embed.set_author(
                        name=f"{ctx.author.name}:", icon_url=ctx.author.avatar_url
                    )
                    embed.add_field(name='Suggestion :', value=f'{suggestion}', inline=False)
                    message_ = await suggestion_channel.send(embed=embed)
                    await message_.add_reaction("<:YES:793374924474810380>")
                    await message_.add_reaction("<:NO:793374924815335437>")
                    await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
        else:
            await ctx.send(embed=discord.Embed(color=self.bot.error_color, title=f"You have been blocked, {ctx.author.name}#{ctx.author.discriminator}.", description=f"Reason: {self.banlist[str(ctx.author.id)]}"))

    @commands.command(aliases=["ssc"])
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def setsuggestchannel(self, ctx, channel: discord.TextChannel):
        """
        Set the channel where suggestions go.
        **Usage**:
        {prefix}setsuggestchannel #suggestions
        {prefix}ssc suggestions
        {prefix}ssc 515085600047628288
        """
        await self.coll.find_one_and_update(
            {"_id": "config"},
            {"$set": {"suggestion-channel": {"channel": str(channel.id)}}},
            upsert=True,
        )
        embed = discord.Embed(
            title=f"Set suggestion channel to #{channel}.", color=0x4DFF73
        )
        embed.set_author(name="Success!")
        embed.set_footer(text="Task succeeded successfully.")
        await ctx.send(embed=embed)

    @commands.command(aliases=["sa"])
    @checks.has_permissions(PermissionLevel.MOD)  
    async def sugaccept(self, ctx, msgID : int, * , reason: str):
        if msgID == None:
            return await ctx.send_help(ctx.command)
  

        config = await self.coll.find_one({"_id": "config"})
        suggestion_channel = self.bot.get_channel(
            int(config["suggestion-channel"]["channel"])
        ) 
        try:
            message = await suggestion_channel.fetch_message(msgID)
            embed  = message.embeds[0] 
        except:
            embed=discord.Embed(title="Please include a valid message ID!", color=0xFF0000)    
            await ctx.send(embed=embed, delete_after = 5.0)

        embed3=embed.copy()
        embed2=discord.Embed(
          color=0x39FF14
        )
        embed2.set_author( 
          name=embed3.author.name, icon_url=embed3.author.icon_url
        )
        autho = embed3.fields[0].name
        embed2.add_field(name=f"✅ {autho} Accepted", value=embed3.fields[0].value, inline=False)
        embed2.add_field(name=f"Reason by : {ctx.author.name}", value=f"{reason}", inline=False)
        await message.edit(embed=embed2)

    @commands.command(aliases=["sn"])
    @checks.has_permissions(PermissionLevel.MOD)  
    async def sugreject(self, ctx, msgID : int, * , reason: str):
        if msgID == None:
            return await ctx.send_help(ctx.command)
  

        config = await self.coll.find_one({"_id": "config"})
        suggestion_channel = self.bot.get_channel(
            int(config["suggestion-channel"]["channel"])
        ) 
        try:
            message = await suggestion_channel.fetch_message(msgID)
            embed  = message.embeds[0] 
        except:
            embed=discord.Embed(title="Please include a valid message ID!", color=0xFF0000)    
            await ctx.send(embed=embed, delete_after = 5.0)

        
        embed3=embed.copy()
        embed2=discord.Embed(
          color=0xff1818
        )
        embed2.set_author( 
          name=embed3.author.name, icon_url=embed3.author.icon_url
        )
        autho = embed3.fields[0].name
        embed2.add_field(name=f"❌ {autho} Rejected", value=embed3.fields[0].value, inline=False)
        embed2.add_field(name=f"Reason by : {ctx.author.name}", value=f"{reason}", inline=False)
        await message.edit(embed=embed2)    
         
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def suggestchannel(self, ctx):
        """Displays the suggestion channel."""
        config = await self.coll.find_one({"_id": "config"})
        suggestion_channel = self.bot.get_channel(
            int(config["suggestion-channel"]["channel"])
        )
        embed = discord.Embed(
            title=f"The suggestion channel is: #{suggestion_channel}",
            description="To change it, use [p]setsuggestchannel.",
            color=0x4DFF73,
        )
        await ctx.send(embed=embed)

    @checks.has_permissions(PermissionLevel.MOD)
    @commands.group(invoke_without_command=True)
    async def suggestmod(self, ctx: commands.Context):
        """Let's you block and unblock people from using the suggest command."""
        await ctx.send_help(ctx.command)

    @suggestmod.command(aliases=["ban"])
    @checks.has_permissions(PermissionLevel.MOD)
    async def block(self, ctx, user: discord.User, *, reason="Reason not specified."):
        """
        Block a user from using the suggest command.
        **Examples:**
        [p]suggestmod block @aniket for abuse!
        [p]suggestmod ban 474255126228500480 `cause he's the same person!!!
        """
        if str(user.id) in self.banlist:
            embed = discord.Embed(
                colour=self.bot.error_color,
                title=f"{user.name}#{user.discriminator} is already blocked.",
                description=f"Reason: {self.banlist[str(user.id)]}",
            )
        else:
            self.banlist[str(user.id)] = reason
            embed = discord.Embed(
                colour=self.bot.main_color,
                title=f"{user.name}#{user.discriminator} is now blocked.",
                description=f"Reason: {reason}",
            )

        await self._update_mod_db()
        await ctx.send(embed=embed)

    @suggestmod.command(aliases=["unban"])
    @checks.has_permissions(PermissionLevel.MOD)
    async def unblock(self, ctx, user: discord.User):
        """
        Unblock a user from using the suggest command.
        **Examples:**
        [p]suggestmod unblock @aniket
        [p]suggestmod unban 474255126228500480
        """
        if str(user.id) not in self.banlist:
            embed = discord.Embed(
                colour=self.bot.error_color,
                title=f"{user.name}#{user.discriminator} is not blocked.",
                description=f"Reason: {self.banlist[str(user.id)]}",
            )
        else:
            self.banlist.pop(str(user.id))
            embed = discord.Embed(
                colour=self.bot.main_color, title=f"{user.name}#{user.discriminator} is now unblocked."
            )

        await self._update_mod_db()
        await ctx.send(embed=embed)    


def setup(bot):
    bot.add_cog(Suggest(bot))
