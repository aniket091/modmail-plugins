import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
from datetime import datetime
import re
from .resources.warn import warnresource

class moderation(commands.Cog):
    """
    Moderation commands to moderate the server!
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.red = 0xfc4343
        self.green = 0x00ff5a
        self.tick = "<:tick:819613405597532160>"
        self.cross = "<:x2:819613332892942347>"
        self.channel = None
        self.bot.loop.create_task(self._set_val())
    
    async def _set_val(self):
       config = await self.db.find_one({"_id": "config"})
       if config is None:
           return

       self.channel = self.bot.get_channel(int(config["channel"]))

    # set modlog channel
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def modlog(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Set the log channel for moderation actions.
        """
        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
        )

        self.channel = self.bot.get_channel(channel.id)
        return await ctx.send(embed = discord.Embed(
             description=f" **{self.tick} Set modlog channel to {channel.mention}!**", color=self.green
        ))

    #Purge command
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def purge(self, ctx, amount = 502):
        """
        Purge certain amount of messages!
        **Usage**:
        {ctx.prefix}purge 10
        """
        if amount == 502:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}purge <amount> \n**Example: **{ctx.prefix}purge 10",
                color = self.red
            )
            return await ctx.send(embed = embed)
            
        max_purge = 500
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                description = f"{self.tick} Purged **{amount}** message(s)!", color = self.green
            )
            await ctx.send(embed = embed, delete_after = 7.0)
            
            embed = discord.Embed(color = self.green, timestamp=datetime.utcnow())
            embed.set_author(name=f"Purge ✂️ | {ctx.message.channel.name}", icon_url=ctx.guild.icon_url)
            embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}", inline=True)
            embed.add_field(name="Channel", value=f"{ctx.message.channel.mention}", inline=True)
            embed.add_field(name="Amount", value=f"{amount}", inline=True)
            await self.channel.send(embed = embed)

        if amount < 1:
            embed = discord.Embed(
                description = f"**{self.cross} You must purge more then `{amount}` message(s)!**",
                color = self.red
            )
            await ctx.send(embed = embed)

        if amount > max_purge:
            embed = discord.Embed(
                description = f"**{self.cross} You must purge less then `500` messages!**",
                color = self.red
            )
            await ctx.send(embed = embed)    



    #kick command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Kicks the specified member.
        **Usage**:
        {ctx.prefix}kick @member 
        {ctx.prefix}kick @member bad!
        """
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}kick <member> [reason]\n**Example: **{ctx.prefix}kick @member\n**Example: **{ctx.prefix}kick @member doing spam!",
                color = self.red
            )
            embed.set_footer(text="<> - Required | [] - optional")
            return await ctx.send(embed = embed)
    
        if member.id == ctx.message.author.id:
            return await ctx.send(embed = await self.errorembed(
                str("You can't kick yourself!")
            ))
        
        if member.guild_permissions.administrator:
            return await ctx.send(embed=await self.errorembed(
                str("That user is an Admin, I can't kick them!!")
            ))
        
        if reason == None:
            await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason provided.")
            await ctx.send(embed = discord.Embed(
                description = f"***{self.tick} {member} has been kicked!***",
                color = self.green
            ))

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been kicked from `{ctx.guild.name}`**",
                    color = self.red
                ))
            except discord.errors.Forbidden:  
                return await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Kick 📑"), str("No reason provided!"), str("I could not DM them.")
                ))
            
            await self.channel.send(embed=await self.log_embed(
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
                    description = f"**You have been kicked from `{ctx.guild.name}` \n*Reason* : {reason}**",
                    color = self.red
                ))
            except discord.errors.Forbidden:
                return await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Kick 📑"), str(reason), str("I could not DM them.")
                ))

            await self.channel.send(embed=await self.log_embed(
                ctx, str(member.id), str("Kick 📑"), str(reason), str("y")
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

        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}ban <member> [reason]\n**Example: **{ctx.prefix}ban @member\n**Example: **{ctx.prefix}ban @member doing spam!",
                color = self.red
            )
            embed.set_footer(text="<> - Required | [] - optional")
            return await ctx.send(embed = embed)
            

        if member.id == ctx.message.author.id:
            return await ctx.send(embed=await self.errorembed(str("You can't ban yourself!")))
            
        if member.guild_permissions.administrator:
            return await ctx.send(embed=await self.errorembed(str("That user is an Admin, I can't ban them!!")))
            
        if reason == None:
            await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}!\nReason - No reason provided.")
            await ctx.send(embed=discord.Embed(
                description = f"***{self.tick} {member} has been banned!***",
                color = self.green
            ))

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been banned from `{ctx.guild.name}`**",
                    color = self.red
                ))
            except discord.errors.Forbidden:  
                return await self.channel.send(embed=await self.loge_mbed(
                    ctx, str(member.id), str("Ban 📑"), str("No reason provided!"), str("I could not DM them.")
                ))
            
            await self.channel.send(embed=await self.log_embed(
                ctx, str(member.id), str("Ban 📑"), str("No reason provided!"), str("y")
            ))
        else:
            await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}!\nReason - {reason}")
            embed = discord.Embed(
                description = f"**{self.tick} {member} has been banned!  || {reason}**",
                color = self.green
            )
            await ctx.send(embed = embed)
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been banned from `{ctx.guild.name}` \n*Reason* : {reason}**",
                    color = self.red
                ))
            except discord.errors.Forbidden:
                return await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Ban 📑"), str(reason), str("I could not DM them.")
                ))

            await self.channel.send(embed=await self.log_embed(
                ctx, str(member.id), str("Ban 📑"), str(reason), str("y")
            ))



    # unban command
    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def unban(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Unbans the specified member.
        **Usage**:
        {ctx.prefix}unban @member 
        """
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}unban [member]\n**Example: **{ctx.prefix}unban @member",
                color = self.red
            )
            return await ctx.send(embed = embed)

        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member.name, member.discriminator):
                await ctx.guild.unban(user)
                await ctx.send(embed=discord.Embed(
                    description = f"{self.tick} **Unbanned `{user.name}`**", color = self.green
                ))
                if reason == None:
                    await self.channel.send(embed=await self.log_embed(
                        ctx, str(member.id), str("Unban 📑"), str(reason), str("y")
                    ))
                else:
                    await self.channel.send(embed=await self.log_embed(
                        ctx, str(member.id), str("Unban 📑"), str("No reason provided!"), str("y")
                    ))


    
    # Mute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Mutes the specified member.
        """
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}mute <member> [reason]\n**Example: **{ctx.prefix}mute @member\n**Example: **{ctx.prefix}mute @member doing spam!",
                color = self.red
            )
            embed.set_footer(text="<> - Required | [] - optional")
            return await ctx.send(embed = embed)

        if member.id == ctx.message.author.id:
            return await ctx.send(embed = await self.errorembed(
                str("You can't mute yourself!")
            ))
        
        role = discord.utils.get(ctx.guild.roles, name = "Muted")
        if role == None:
            role = await ctx.guild.create_role(name = "Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(role, send_messages = False)
        await member.add_roles(role)
        
        if reason == None:
            embed = discord.Embed(
                description = f"**{self.tick} {member} has been muted!**", color = self.green
            )
            await ctx.send(embed = embed)

            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been muted in `{ctx.guild.name}`**", color = self.red
                ))
            except discord.errors.Forbidden:
                return await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Mute 🔇"), str("No reason provided!"), str("I could not DM them.")
                ))

            await self.channel.send(embed=await self.log_embed(
                ctx, str(member.id), str("Mute 🔇"), str("No reason provided!"), str("y")
            ))

        else:
            embed = discord.Embed(
                description = f"**{self.tick} {member} has been muted!  || {reason}**", color = self.green
            )
            await ctx.send(embed = embed)
                
            try:
                await member.send(embed=discord.Embed(
                    description = f"**You have been muted in `{ctx.guild.name}` \n*Reason* : {reason}**",
                    color = self.red
                ))
            except discord.errors.Forbidden:
                return await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Mute 🔇"), str(reason), str("I could not DM them.")
                ))

            await self.channel.send(embed=await self.log_embed(
                ctx, str(member.id), str("Mute 🔇"), str(reason), str("y")
            ))  
    

    
    # unmute command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unmute(self, ctx, member : discord.Member = None, *, reason = None):
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
                description = f"**Usage: **{ctx.prefix}unmute [member] [reason]\n**Example: **{ctx.prefix}unmute @member",
                color = self.red
            )
            return await ctx.send(embed = embed)
            

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
                    color = self.green
                ))
            except discord.errors.Forbidden:
                if reason == None:
                    await self.channel.send(embed=await self.log_embed(
                        ctx, str(member.id), str("Unmute 🔉"), str("No reason provided!"), str("I could not DM them.")
                    ))
                else:
                    await self.channel.send(embed=await self.log_embed(
                        ctx, str(member.id), str("Unmute 🔉"), str(reason), str("I could not DM them.")
                    ))    
            
            if reason == None:
                await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Unmute 🔉"), str("No reason provided!"), str("y")
                ))
            else:
                await self.channel.send(embed=await self.log_embed(
                    ctx, str(member.id), str("Unmute 🔉"), str(reason), str("y")
                ))

        else:
            return await ctx.send(embed = await self.errorembed(
                str(f"{member.name} is not muted!")
            ))

    # delwarn command
    @commands.command(aliases = [""])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def delwarn(self, ctx, member : discord.Member = None, *, num = None):
        """Delete warn of a member.
        Usage:
        {ctx.prefix}warns @member
        """
        await warnresource(ctx, self.bot, self.db, self.channel, member).delwarn(num)
     
    # warns command
    @commands.command(aliases = ["warnings"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def warns(self, ctx, member : discord.Member = None):
        """Show warns of a member.
        Usage:
        {ctx.prefix}warns @member
        """
        await warnresource(ctx, self.bot, self.db, self.channel, member).warns()

    # warn command
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def warn(self, ctx, member : discord.Member = None, *, reason = None):
        """Warn a member.
        Usage:
        {ctx.prefix}warn @member reason
        """
        await warnresource(ctx, self.bot, self.db, self.channel, member).warn(reason)


    #SLOW MODE COMMAND
    @commands.command(aliases=["sm"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode(self, ctx, time = None, channel: discord.TextChannel = None):
        """Set a slowmode to a channel
        It is not possible to set a slowmode longer than 6 hours
        **Usage**:
        {ctx.prefix}slowmode 5s
        {ctx.prefix}slowmode 1h
        """
        if time == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}sm [time] [channel]\n**Example: **{ctx.prefix}sm 5s\n**Example: **{ctx.prefix}sm 5s #channel",
                color = self.red
            )
            return await ctx.send(embed = embed)

        if channel == None:
            channel = ctx.channel

        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", time)
        if not match:
            embed = discord.Embed(description=f"**{self.cross} I cannot understand your time format!**",color = self.red)
            return await ctx.send(embed=embed)
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        if seconds > 21600:
            embed = discord.Embed(description=f"**{self.cross} You can't slowmode a channel for longer than 6 hours!**", color=self.red)
            return await ctx.send(embed=embed)
        try:
            await channel.edit(slowmode_delay=seconds)
        except discord.errors.Forbidden:
            embed = discord.Embed(description=f"**{self.cross} I don't have permission to do this!**", color=self.red)
            return await ctx.send(embed=embed)
        embed=discord.Embed(description=f"**{self.tick} Set a slowmode delay of `{time}` in {channel.mention}**", color=self.green)
        await ctx.send(embed=embed)

        embed = discord.Embed(color = self.green, timestamp=datetime.utcnow())
        embed.set_author(name=f"Slowmode Enabled ⏱️| {channel.name}", icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"Moderator ", value=f"{ctx.message.author.mention}", inline=False)
        embed.add_field(name=f"Channel ", value=f"{channel.mention}", inline=False)
        embed.add_field(name=f"Time", value=f"{time}", inline=False)   
        await self.channel.send(embed=embed)

    # slowmode off
    @commands.command(aliases=["sm-off", "smoff"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode_off(self, ctx, channel: discord.TextChannel = None):
        """Turn off the slowmode in a channel"""
        if not channel:
            channel = ctx.channel

        seconds_off = 0
        await channel.edit(slowmode_delay=seconds_off)
        embed=discord.Embed(description=f"**{self.tick} Turned off the slowmode for {channel.mention}**", color=self.green)
        await ctx.send(embed=embed)    
        embed = discord.Embed(color = 0x00dcff, timestamp=datetime.utcnow())
        embed.set_author(name=f"Slowmode Disabled ⏱️ | {channel.name}", icon_url=ctx.guild.icon_url)
        embed.add_field(name=f"Moderator ", value=f"{ctx.message.author.mention}", inline=False)
        embed.add_field(name=f"Channel ", value=f"{channel.mention}", inline=False)  
        await self.channel.send(embed=embed)


    async def log_embed(self, ctx, memberid, action, reason, status):
        """log embed for moderation commands"""
        member: discord.User = await self.bot.fetch_user(int(memberid))
        if action == "Mute 🔇":
            color = 0xffdd57
        else:
            color = self.green    
        embed  = discord.Embed(color = color, timestamp=datetime.utcnow())
        embed.set_author(name=f"{action} | {member}", icon_url=member.avatar_url)
        embed.add_field(name="User", value=f"{member.mention}", inline=True)
        embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}", inline=True)
        embed.add_field(name="Channel", value=f"{ctx.message.channel.mention}", inline=True)
        embed.add_field(name="Reason ", value=reason, inline=False)
        embed.set_footer(text=f"ID: {member.id}")
        if status != "y":
            embed.add_field(name="Status", value=status, inline=False)
        return embed

    async def errorembed(self, error):
        embed = discord.Embed(description = f"{self.cross}  **{error}**", color = self.red)
        return embed  
    
        
def setup(bot):
    bot.add_cog(moderation(bot))