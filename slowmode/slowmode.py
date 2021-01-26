import discord
from discord.ext import commands
import re
from core import checks
from core.models import PermissionLevel

class SlowMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='[duration] [channel]')
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode(self, ctx: commands.Context, *, time: UserFriendlyTime(converter=commands.TextChannelConverter, default=False, assume_reason=True)) -> None:
        """Enables slowmode, max 6h
        Examples:
        !!slowmode 2h
        !!slowmode 2h #general
        !!slowmode off
        !!slowmode 0s #general
        """
        duration = timedelta()
        channel = ctx.channel
        if time.dt:
            duration = time.dt - ctx.message.created_at
        if time.arg:
            if isinstance(time.arg, str):
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, time.arg)
                except commands.BadArgument:
                    if time.arg != 'off':
                        raise
            else:
                channel = time.arg

        seconds = int(duration.total_seconds())

        if seconds > 21600:
            await ctx.send('Slowmode only supports up to 6h max at the moment')
        else:
            fmt = format_timedelta(duration, assume_forever=False)
            await channel.edit(slowmode_delay=int(duration.total_seconds()))
            if duration.total_seconds():
                await ctx.send(f'Enabled `{fmt}` slowmode on {channel.mention}')
            else:
                await ctx.send(f'Disabled slowmode on {channel.mention}')

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode_off(self, ctx, channel: discord.TextChannel = None):
        """Turn off the slowmode in a channel"""
        if not channel:
            channel = ctx.channel
        seconds_off = 0
        await channel.edit(slowmode_delay=seconds_off)
        embed=discord.Embed(description=f"{ctx.author.mention} turned off the slowmode in {channel.mention}", color=0x06c9ff)
        embed.set_author(name="Slow Mode")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            # This is the same as the elif except it handles agaisnt empty overwrites dicts
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"I have put {channel.name} on lockdown.")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have put {channel.name} on lockdown.")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"I have removed {channel.name} from lockdown.")


def setup(bot):
    bot.add_cog(SlowMode(bot))
