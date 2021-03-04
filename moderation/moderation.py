import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

class moderation(commands.Cog):
    """
    Moderation commands to moderate the server!😼
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.errorcolor = 0xe60026
        self.bluee = 0x09eb10
        self.greenn = 0x4fe8a2
        self.yell = 0xffe945

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
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Set the log channel for moderation actions.
        """

        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
        )

        await ctx.send("Done!")
        return

    #Purge command
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def purge(self, ctx, amount = 10, member : discord.Member = None):
        """
        Purge certain amount of messages!
        """
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))


        max_purge = 2000
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                title = "Purge 📑",
                description = f"✅ Purged **{amount}** message(s)!",
                color = self.bluee
            )
            await ctx.send(embed = embed, delete_after = 10.0)
            embed = discord.Embed(
                title = "Purge 📑",
                color = self.greenn
            )
            embed.add_field(name="Amount :", value=f"**{amount}**", inline=True)
            embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
            embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
            await channel.send(embed = embed)
        if amount < 1:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"❌ You must purge more then {amount} message(s)!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()
        if amount > max_purge:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"❌ You must purge less then {amount} messages!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "❌ You are missing permissions to purge messages!",
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
        """
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))

    
        if member == None:
            embed = discord.Embed(
                description = "❌ **Please specify a member!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    description = "❌ **You can't kick yourself!**",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if member.guild_permissions.administrator:
                    embed = discord.Embed(
                        description = "❌ **That user is a Admin, I can't kick them!**",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:    
                    if reason == None:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
                        msg = f"You have been kicked from {ctx.guild.name}"
                        embed = discord.Embed(
                            description = f"***✅ {member} has been kicked!***",
                            color = self.bluee
                        )
                        await ctx.send(embed = embed)
                        await member.send(msg)
                        embedlog = discord.Embed(
                            color = self.greenn
                        )
                        embedlog.set_author(
                            name=f"Kick 📑 | {member}",
                            icon_url=member.avatar_url,
                        )
                        embedlog.add_field(name="User Kicked :", value=f"{member.mention}", inline=True)
                        embedlog.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                        embedlog.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                        embedlog.add_field(name="Reason :", value="No reason provided!", inline=False)
                        await channel.send(embed = embedlog)

                        msg = f"You have been kicked from **{ctx.guild.name}**"
                        try:
                            await member.send(msg)
                        except discord.errors.Forbidden:
                            return await channel.send(
                                embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                            )
                    else:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                        
                        embed = discord.Embed(
                            description = f"**✅ {member} has been kicked!** \n**|| {reason}**",
                            color = self.bluee
                        )
                        await ctx.send(embed = embed)
                        embedlog = discord.Embed(
                            color = self.greenn
                        )
                        embedlog.set_author(
                            name=f"Kick 📑 | {member}",
                            icon_url=member.avatar_url,
                        )
                        embedlog.add_field(name="User Kicked :", value=f"{member.mention}", inline=True)
                        embedlog.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                        embedlog.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                        embedlog.add_field(name="Reason :", value=f"{reason}", inline=False)
                        await channel.send(embed = embedlog)
                        
                        msg = f"You have been kicked from **{ctx.guild.name}** for `{reason}`"
                        try:
                            await member.send(msg)
                        except discord.errors.Forbidden:
                            return await channel.send(
                                embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                            )
                        
                        
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions !",
                description = "❌ You are missing permissions to kick members!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Ban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Bans the specified member.
        """
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))


        if member == None:
            embed = discord.Embed(
                description = "❌ **Please specify a member!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    description = "❌ **You can't kick yourself!**",
                    color = self.blurple
                )
                await ctx.send(embed = embed)
            else:
                if member.guild_permissions.administrator:
                    embed = discord.Embed(
                        description = "❌ **That user is a Admin, I can't ban them!**",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:    
                    if reason == None:
                        await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No Reason Provided.")
                        embed = discord.Embed(
                            description = f"***✅ {member} has been banned !***",
                            color = self.bluee
                        )
                        await ctx.send(embed = embed)
                        embedlog = discord.Embed(
                            color = self.greenn
                        )
                        embedlog.set_author(
                            name=f"Ban 📑 | {member}",
                            icon_url=member.avatar_url,
                        )
                        embedlog.add_field(name="User Banned :", value=f"{member.mention}", inline=True)
                        embedlog.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                        embedlog.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                        embedlog.add_field(name="Reason :", value="No reason provided!", inline=False)
                        await channel.send(embed = embedlog)
                        
                        msg = f"You have been banned from **{ctx.guild.name}**"
                        try:
                            await member.send(msg)
                        except discord.errors.Forbidden:
                            return await channel.send(
                                embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                            )
                    else:
                        await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                        embed = discord.Embed(
                            description = f"***✅ {member} has been banned !*** \n**|| {reason}**",
                            color = self.bluee
                        )
                        await ctx.send(embed = embed)
                        embedlog = discord.Embed(
                            color = self.greenn
                        )
                        embedlog.set_author(
                            name=f"Ban 📑 | {member}",
                            icon_url=member.avatar_url,
                        )
                        embedlog.add_field(name="User Banned :", value=f"{member.mention}", inline=True)
                        embedlog.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                        embedlog.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                        embedlog.add_field(name="Reason :", value=f"{reason}", inline=False)
                        await channel.send(embed = embedlog)
                        
                        msg = f"You have been banned from **{ctx.guild.name}** for `{reason}`"
                        try:
                            await member.send(msg)
                        except discord.errors.Forbidden:
                            return await channel.send(
                                embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                            )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "❌ **You are missing permissions to ban members!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Unban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unban(self, ctx, *, member : discord.User = None):
        """
        Unbans the specified member.
        """
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))


        if member == None:
            embed = discord.Embed(
                title = "Unban Error!",
                description = "❌ **Please specify a user!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member.name, member.discriminator):
                    embed = discord.Embed(
                        title = "Unban",
                        description = f"✅ **Unbanned {user.mention}**",
                        color = self.bluee
                    )
                    await ctx.guild.unban(user)
                    await ctx.send(embed = embed)
                    embed = discord.Embed(
                        title = "Unban 📑",
                        color = self.yell
                    )
                    embed.add_field(name="User UnBanned :", value=f"{member.mention}", inline=True)
                    embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                    embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                    await channel.send(embed = embed)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "❌ **You are missing permission to unban peole**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

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
                title = "Mute Error!",
                description = "❌ **Please specify a user!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Mute Error!",
                    description = "❌ **You can't mute yourself!**",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                if reason == None:
                    role = discord.utils.get(ctx.guild.roles, name = "Muted")
                    if role == None:
                        role = await ctx.guild.create_role(name = "Muted")
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(role, send_messages = False)
                    await member.add_roles(role)
                    embed = discord.Embed(
                        description = f"***{member} has been muted !***",
                        color = self.bluee
                    )
                    await ctx.send(embed = embed)
                    embed = discord.Embed(
                        color = self.greenn
                    )
                    embed.set_author(
                        name=f"Mute 🔇 | {member}",
                        icon_url=member.avatar_url,
                    )
                    embed.add_field(name="User Muted :", value=f"{member.mention}", inline=True)
                    embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                    embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                    await channel.send(embed = embed)

                    msg = f"You have been muted in **{ctx.guild.name}** "
                    try:
                        await member.send(msg)
                    except discord.errors.Forbidden:
                        return await channel.send(
                            embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                        )
                else:
                    role = discord.utils.get(ctx.guild.roles, name = "Muted")
                    if role == None:
                        role = await ctx.guild.create_role(name = "Muted")
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(role, send_messages = False)
                    await member.add_roles(role)
                    embed = discord.Embed(
                        description = f"***✅ {member} has been muted !*** \n**|| {reason}**",
                        color = self.bluee
                    )
                    await ctx.send(embed = embed)
                    embed = discord.Embed(
                        color = self.greenn
                    )
                    embed.set_author(
                        name=f"Mute 🔇 | {member}",
                        icon_url=member.avatar_url,
                    )
                    embed.add_field(name="User Muted :", value=f"{member.mention}", inline=True)
                    embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                    embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                    embed.add_field(name="Reason :", value=f"{reason}", inline=False)
                    await channel.send(embed = embed)

                    msg = f"You have been muted in **{ctx.guild.name}** for `{reason}`"
                    try:
                        await member.send(msg)
                    except discord.errors.Forbidden:
                        return await channel.send(
                            embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                        )

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "❌ **You are missing permission to mute people!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Unmute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unmute(self, ctx, member : discord.Member = None):
        """
        Unmutes the specified member.
        """
        channel_config = await self.db.find_one({"_id": "config"})

        if channel_config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(channel_config["channel"]))


        if member == None:
            embed = discord.Embed(
                title = "Unmute Error!",
                description = "❌ **Please specify a user!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            role = discord.utils.get(ctx.guild.roles, name = "Muted")
            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(
                    description = f"***✅ {member} has been unmuted!***",
                    color = self.bluee
                )
                await ctx.send(embed = embed)
                embed = discord.Embed(
                    color = self.greenn
                )
                embed.set_author(
                    name=f"Unmute 🔉 | {member}",
                    icon_url=member.avatar_url,
                )
                embed.add_field(name="User UnMuted :", value=f"{member.mention}", inline=True)
                embed.add_field(name="Moderator :", value=f"{ctx.message.author.mention}", inline=True)
                embed.add_field(name="Channel :", value=f"{ctx.message.channel.mention}", inline=True)
                await channel.send(embed = embed)

                msg = f"You have been unmuted in **{ctx.guild.name}** for `{reason}`"
                try:
                    await member.send(msg)
                except discord.errors.Forbidden:
                    return await channel.send(
                        embed=discord.Embed(description='Member has been kicked , they i was unable to DM them!')
                    )
            else:
                embed = discord.Embed(
                    title = "Unmute Error!",
                    description = f"**❌ {member.mention} is not muted!**",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "❌ **You are missing permission to unmute people!**",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
            
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warn a member.
        Usage:
        {prefix}warn @member Spoilers
        """

        if member.bot:
            return await ctx.send("Bots can't be warned.")

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

        embed = discord.Embed(
            description = f"✅  ***{member} has been warned.***\n**|| {reason}**",
            color = self.bluee
        )
        await ctx.send(embed = embed)
        await member.send(f'You have been warned in {ctx.guild.name} for {reason}')

        await channel.send(
            embed=await self.generateWarnEmbed(
                str(member.id), str(ctx.author.id), len(userw), reason
            )
        )
        del userw
        return

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def pardon(self, ctx, member: discord.Member, *, reason: str):
        """Remove all warnings of a  member.
        Usage:
        {prefix}pardon @member Nice guy
        """

        if member.bot:
            return await ctx.send("❌ Bots can't be warned, so they can't be pardoned.")

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
            embed = discord.Embed(
                description = f"**❌ {member} doesn't have any warnings.**",
                color = self.errorcolor
            )
            return await ctx.send(embed = embed)

        if userwarns is None:
            embedtwo = discord.Embed(
                description = f"**❌ {member} doesn't have any warnings.**",
                color = self.errorcolor
            )
            await ctx.send(embed = embedtwo)

        await self.db.find_one_and_update(
            {"_id": "warns"}, {"$set": {str(member.id): []}}
        )

        embedfinal = discord.Embed(
                description = f"<:tick:811926934220046346>  ***{member} has been pardoned.***\n**|| {reason}**",
                color = self.bluee
            )
        await ctx.send(embed = embedfinal)

        embed = discord.Embed(color = self.greenn)

        embed.set_author(
            name=f"Pardon | {member}",
            icon_url=member.avatar_url,
        )
        embed.add_field(name="User :", value=f"{member}", inline = True)
        embed.add_field(
            name="Moderator :",
            value=f"<@{ctx.author.id}>",
            inline = True,
        )
        embed.add_field(name="Total Warnings :", value="0", inline = True)
        embed.add_field(name="Reason :", value=reason, inline = False)

        return await channel.send(embed=embed)

    async def generateWarnEmbed(self, memberid, modid, warning, reason):
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
        return embed


def setup(bot):
    bot.add_cog(moderation(bot))
