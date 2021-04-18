import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import re
import asyncio

class moderation(commands.Cog):
    """
    Moderation commands to moderate the server!
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.errorcolor = 0xfc4343
        self.blue = 0x3ef7e8
        self.green = 0x00ff5a
        self.yell = 0xfffc36
        self.tick = "<:tick:819613405597532160>"
        self.cross = "<:x2:819613332892942347>"

    #On channel create set up mute stuff
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            role = await guild.create_role(name = "Muted")
        await channel.set_permissions(role, send_messages = False)
   
    #log channel
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def modlog(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Set the log channel for moderation actions.
        """
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
        )
        embed = discord.Embed(
            description=f" **{self.tick} Set modlog channel to {channel.mention}!**", color=self.green
        )
        await ctx.send(embed=embed)
        return

    #Purge command
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def purge(self, ctx, amount = 2, member : discord.Member = None):
        """
        Purge certain amount of messages!
        **Usage**:
        {ctx.prefix}purge 10
        {ctx.prefix}purge 10 @Aniket
        {ctx.prefix}purge <amount> [member]
        """
        #get-channel
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        max_purge = 500
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                description = f"{self.tick} Purged **{amount}** message(s)!",
                color = self.green
            )
            await ctx.send(embed = embed, delete_after = 10.0)
            embed = discord.Embed(
                title = "Purge 📑",
                color = self.green
            )
            embed.add_field(name="Amount :", value=f"**{amount}**", inline=True)
            embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
            embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
            await channel.send(embed = embed)
        if amount < 1:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"**{self.cross} You must purge more then `{amount}` message(s)!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()
        if amount > max_purge:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"**{self.cross} You must purge less then `{amount}` messages!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "**{self.cross} You are missing permissions to purge messages!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()


    #Kick command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Kicks the specified member.
        **Usage**:
        {ctx.prefix}kick @member 
        {ctx.prefix}kick @member bad!
        """
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}kick <member> [reason]\n**Example: **{ctx.prefix}kick @member\n**Example: **{ctx.prefix}kick @member doing spam!",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required | [] - optional")
            await ctx.send(embed = embed)
            return

        if member.id == ctx.message.author.id:
            await ctx.send(embed=await self.errorembed(str("You can't kick yourself!")))
            return

        if member.guild_permissions.administrator:
            await ctx.send(embed=await self.errorembed(str("That user is an Admin, I can't kick them!!")))
            return

        if reason == None:
            await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
            await ctx.send(embed=discord.Embed(
                description = f"***{self.tick} {member} has been kicked!***",
                color = self.green
            ))

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been kicked from `{ctx.guild.name}`**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:  
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Kick 📑"), str("No reason provided!"), str("I could not DM them.")
                ))
            
            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Kick 📑"), str("No reason provided!"), str("y")
            ))
        else:
            await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
            embed = discord.Embed(
                description = f"**{self.tick} {member} has been kicked!  || {reason}**",
                color = self.green
            )
            await ctx.send(embed = embed)
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been kicked from `{ctx.guild.name}` \n\nReason :- {reason}**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Kick 📑"), str(reason), str("I could not DM them.")
                ))

            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Kick 📑"), str(reason), str("y")
            ))
                                               
                        
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title = "Missing Permissions!",
                description = f"{self.cross} **You are missing permissions to kick members!**",
                color = self.errorcolor
            ))
            


    #Ban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Bans the specified member.
        **Usage**:
        {ctx.prefix}ban @member 
        {ctx.prefix}ban @member bad!
        """
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}ban <member> [reason]\n**Example: **{ctx.prefix}ban @member\n**Example: **{ctx.prefix}ban @member doing spam!",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required | [] - optional")
            await ctx.send(embed = embed)
            return

        if member.id == ctx.message.author.id:
            await ctx.send(embed=await self.errorembed(str("You can't ban yourself!")))
            return

        if member.guild_permissions.administrator:
            await ctx.send(embed=await self.errorembed(str("That user is an Admin, I can't ban them!!")))
            return

        if reason == None:
            await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
            await ctx.send(embed=discord.Embed(
                description = f"***{self.tick} {member} has been banned!***",
                color = self.green
            ))

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been banned from `{ctx.guild.name}`**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:  
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Ban 📑"), str("No reason provided!"), str("I could not DM them.")
                ))
            
            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Ban 📑"), str("No reason provided!"), str("y")
            ))
        else:
            await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
            embed = discord.Embed(
                description = f"**{self.tick} {member} has been banned!  || {reason}**",
                color = self.green
            )
            await ctx.send(embed = embed)
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been banned from `{ctx.guild.name}` \n\nReason :- {reason}**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Ban 📑"), str(reason), str("I could not DM them.")
                ))

            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Ban 📑"), str(reason), str("y")
            ))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title = "Missing Permissions!",
                description = f"{self.cross} **You are missing permissions to ban members!**",
                color = self.errorcolor
            ), delete_after = 5.0)


    #Unban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unban(self, ctx, *, member : discord.User = None):
        """
        Unbans the specified member.
        **Usage**:
        {ctx.prefix}unban @member 
        """
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}unban <member>\n**Example: **{ctx.prefix}unban @member",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required")
            await ctx.send(embed = embed)
        else:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member.name, member.discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(embed=discord.Embed(
                        description = f"{self.tick} **Unbanned `{user.name}`**",
                        color = self.green
                    ))
                    embed = discord.Embed(title = "Unban 📑", color = self.yell)
                    embed.add_field(name="User UnBanned :", value=f"{member.mention}", inline=True)
                    embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                    embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                    await channel.send(embed = embed)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(
                title = "Missing Permissions!",
                description = f"{self.cross} **You are missing permission to unban peole**",
                color = self.errorcolor
            ), delete_after = 5.0)

    #Mute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Mutes the specified member.
        """
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))


        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}mute <member> [reason]\n**Example: **{ctx.prefix}mute @member\n**Example: **{ctx.prefix}mute @member doing spam!",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required | [] - optional")
            return await ctx.send(embed = embed)

        if member.id == ctx.message.author.id:
            return await ctx.send(embed = discord.Embed(
                description = f"{self.cross} **You can't mute yourself!**",
                color = self.errorcolor
            ), delete_after = 5.0)

        if reason == None:
            role = discord.utils.get(ctx.guild.roles, name = "Muted")
            if role == None:
                role = await ctx.guild.create_role(name = "Muted")
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(role, send_messages = False)
            await member.add_roles(role)
            embed = discord.Embed(
                description = f"{self.tick} ***{member} has been muted !***",
                color = self.green
            )
            await ctx.send(embed = embed)

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been muted in `{ctx.guild.name}`**",
                color = self.blue
                ))
            except discord.errors.Forbidden:
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Mute 🔇"), str("No reason provided!"), str("I could not DM them.")
                ))

            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Mute 🔇"), str("No reason provided!"), str("y")
            ))

        else:
            role = discord.utils.get(ctx.guild.roles, name = "Muted")
            if role == None:
                role = await ctx.guild.create_role(name = "Muted")
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(role, send_messages = False)
            await member.add_roles(role)
            embed = discord.Embed(
                description = f"***{self.tick} {member} has been muted !  || {reason}**",
                color = self.green
            )
            await ctx.send(embed = embed)
                
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been muted in `{ctx.guild.name}` || {reason}**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:
                return await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Mute 🔇"), str(reason), str("I could not DM them.")
                ))

            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Mute 🔇"), str(reason), str("y")
            ))    



    #Unmute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unmute(self, ctx, member : discord.Member = None):
        """
        Unmutes the specified member.
        **Usage**:
        {ctx.prefix}mute @member 
        """
        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}unmute <member> [reason]\n**Example: **{ctx.prefix}unmute @member",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required | [] - optional")
            await ctx.send(embed = embed)
            return

        role = discord.utils.get(ctx.guild.roles, name = "Muted")
        if role in member.roles:
            await member.remove_roles(role)

            await ctx.send(embed=discord.Embed(
                description = f"***{self.tick} {member} has been unmuted!***",
                color = self.green
            ))      
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been unmuted in `{ctx.guild.name}`**",
                    color = self.blue
                ))
            except discord.errors.Forbidden:
                await channel.send(embed=await self.logembed(
                    ctx, str(member.id), str("Unmute 🔉"), str("No reason provided!"), str("I could not DM them.")
                ))

            await channel.send(embed=await self.logembed(
                ctx, str(member.id), str("Unmute 🔉"), str("No reason provided!"), str("y")
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title = "Unmute Error!",
                description = f"**{self.cross} {member.mention} is not muted!**",
                color = self.errorcolor
            ))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title = "Missing Permissions!",
                description = f"{self.cross} **You are missing permission to unmute people!**",
                color = self.errorcolor
            ))

    #warn command        
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def warn(self, ctx, member : discord.Member = None, *, reason: str):
        """Warn a member.
        Usage:
        {ctx.prefix}warn @member reason
        """
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}warn <member> <reason>\n**Example: **{ctx.prefix}warn @member doing spam!",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required")
            return await ctx.send(embed = embed)

        if member.bot:
            return await ctx.send(embed=discord.Embed(
                description = f"**{self.cross} Bots can't be warned.**",
                color = self.errorcolor
            ))

        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if channel is None:
            return

        config = await self.db.find_one({"_id": "warns"})
        if config is None:
            config = await self.db.insert_one({"_id": "warns"})

        try:
            userwarns = config[str(member.id)]
        except KeyError:
            userwarns = config[str(member.id)] = []

        if userwarns is None:
            userw = []
        else:
            userw = userwarns.copy()

        userw.append({"reason": reason, "mod": ctx.author.id})

        await self.db.find_one_and_update(
            {"_id": "warns"}, {"$set": {str(member.id): userw}}, upsert=True
        )

        await ctx.send(embed = discord.Embed(
            description = f"{self.tick} ***{member} has been warned!  || {reason}**",
            color = self.green
        ))
                        
        try:
            await member.send(embed=discord.Embed(
                description = f"**You have been warned in `{ctx.guild.name}`\n|| {reason}**",
                color = self.blue
            ))
        except discord.errors.Forbidden:
            return await channel.send(embed=await self.generateWarnEmbed(
                str(member.id), str(ctx.author.id), len(userw), reason, str("I could not DM them.")
            )) 

        await channel.send(
            embed=await self.generateWarnEmbed(
                str(member.id), str(ctx.author.id), len(userw), reason
            )
        )
        del userw
        return

    #pardon
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def pardon(self, ctx, member: discord.Member = None, *, reason: str):
        """Remove all warnings of a  member.
        Usage:
        {ctx.prefix}pardon @member Nice guy
        """
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}pardon <member> <reason>\n**Example: **{ctx.prefix}pardon @member doing spam!",
                color = self.errorcolor
            )
            embed.set_footer(text="<> - Required")
            return await ctx.send(embed = embed)

        if member.bot:
            return await ctx.send(embed=discord.Embed(
                description = f"**{self.cross} Bots can't be warned, so they can't be pardoned.**",
                color = self.errorcolor
            ))

        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

        if channel is None:
            return

        config = await self.db.find_one({"_id": "warns"})

        if config is None:
            return

        try:
            userwarns = config[str(member.id)]
        except KeyError:
            return await ctx.send(embed = discord.Embed(
               description = f"**{self.cross} {member} doesn't have any warnings.**",
                color = self.errorcolor 
            ))

        if userwarns is None:
            await ctx.send(embed = discord.Embed(
                description = f"**{self.cross} {member} doesn't have any warnings.**",
                color = self.errorcolor
            ))

        await self.db.find_one_and_update(
            {"_id": "warns"}, {"$set": {str(member.id): []}}
        )

        embedfinal = discord.Embed(
                description = f"{self.tick} ***{member} has been pardoned.***\n**|| {reason}**",
                color = self.green
            )
        await ctx.send(embed = embedfinal)
        
        await channel.send(embed=await self.generateWarnEmbed(
            str(member.id), str(ctx.author.id), str("0"), reason
        ))

    
    #SLOW MODE COMMAND
    @commands.command(aliases=["sm"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode(self, ctx, time, channel: discord.TextChannel = None):
        """Set a slowmode to a channel
        It is not possible to set a slowmode longer than 6 hours
        **Usage**:
        {ctx.prefix}slowmode 5s
        {ctx.prefix}slowmode 1h
        """
        if channel == None:
            channel = ctx.channel

        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            logchannel = ctx.guild.get_channel(int(channel_config["channel"]))

        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", time)
        if not match:
            embed = discord.Embed(description=f"**{self.cross} I cannot understand your time format!**",color = self.errorcolor)
            return await ctx.send(embed=embed)
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        if seconds > 21600:
            embed = discord.Embed(description=f"**{self.cross} You can't slowmode a channel for longer than 6 hours!**", color=self.errorcolor)
            return await ctx.send(embed=embed)
        try:
            await channel.edit(slowmode_delay=seconds)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"**{self.cross} I don't have permission to do this!**", color=self.errorcolor)
            return await ctx.send(embed=embed)
        embed=discord.Embed(description=f"**{self.tick} Set a slowmode delay of `{time}` in {channel.mention}**", color=self.green)
        await ctx.send(embed=embed)

        embed = discord.Embed(color = self.green)
        embed.set_author(name=f"Slowmode Enabled", icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"Moderator :", value=f"{ctx.message.author.mention}", inline=False)
        embed.add_field(name=f"Channel :", value=f"{channel.mention}", inline=False)
        embed.add_field(name=f"Time", value=f"{time}", inline=False)   
        await logchannel.send(embed=embed)

    @commands.command(aliases=["sm-off", "smoff"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode_off(self, ctx, channel: discord.TextChannel = None):
        """Turn off the slowmode in a channel"""
        if not channel:
            channel = ctx.channel

        channel_config = await self.db.find_one({"_id": "config"})
        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            logchannel = ctx.guild.get_channel(int(channel_config["channel"]))

        seconds_off = 0
        await channel.edit(slowmode_delay=seconds_off)
        embed=discord.Embed(description=f"**{self.tick} Turned off the slowmode for {channel.mention}**", color=self.green)
        await ctx.send(embed=embed)    
        embed = discord.Embed(color = self.blue)
        embed.set_author(name=f"Slowmode Disabled", icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"Moderator :", value=f"{ctx.message.author.mention}", inline=False)
        embed.add_field(name=f"Channel :", value=f"{channel.mention}", inline=False)  
        await logchannel.send(embed=embed)

    async def generateWarnEmbed(self, memberid, modid, warning, reason, status):
        member: discord.User = await self.bot.fetch_user(int(memberid))
        mod: discord.User = await self.bot.fetch_user(int(modid))

        embed = discord.Embed(color = self.yell)

        embed.set_author(
            name=f"Warn | {member}",
            icon_url=member.avatar_url,
        )
        embed.add_field(name="User Warn :", value=f"{member}", inline = True)
        embed.add_field(name="Moderator :", value=f"<@{modid}>", inline = True)
        embed.add_field(name="Total Warnings :", value=warning, inline = False)
        embed.add_field(name="Reason :", value=reason, inline = False)
        if status:
            embed.add_field(name="Status :", value=status, inline=False)

        return embed

    async def errorembed(self, error):
        embed = discord.Embed(
            description = f"{self.cross}  **{error}**",
            color = self.errorcolor
        )
        return embed   

    async def logembed(self, ctx, memberid, mod, reason, status):
        member: discord.User = await self.bot.fetch_user(int(memberid))

        embed  = discord.Embed(color = self.green)
        embed.set_author(name=f"{mod} | {member}", icon_url=member.avatar_url)
        embed.add_field(name="User Kicked :", value=f"{member.mention}", inline=True)
        embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
        embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=False)
        embed.add_field(name="Reason :", value=reason, inline=False)
        if status != "y":
            embed.add_field(name="Status :", value=status, inline=False)

        return embed      
  

def setup(bot):
    bot.add_cog(moderation(bot))
