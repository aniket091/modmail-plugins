import discord
from discord.ext import commands
import re
from core import checks
from core.models import PermissionLevel

class SlowMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def slowmode(self, ctx, time, channel: discord.TextChannel = None):
        """Set a slowmode to a channel
        It is not possible to set a slowmode longer than 6 hours
        """
        if not channel:
            channel = discord.TextChannel = None

        units = {
            "d": 86400,
            "h": 3600,
            "m": 60,
            "s": 1
        }
        seconds = 0
        match = re.findall("([0-9]+[smhd])", time)
        if not match:
            embed = discord.Embed(description="⚠ I dont understand your time format!",color = 0xff0000)
            return await ctx.send(embed=embed)
        for item in match:
            seconds += int(item[:-1]) * units[item[-1]]
        if seconds > 21600:
            embed = discord.Embed(description="⚠ You can't slowmode a channel for longer than 6 hours!", color=0xff0000)
            return await ctx.send(embed=embed)
        try:
            await channel.edit(slowmode_delay=seconds)
        except discord.errors.Forbidden:
            embed = discord.Embed(description="⚠ I don't have permission to do this!", color=0xff0000)
            return await ctx.send(embed=embed)
        embed=discord.Embed(description=f"{ctx.author.mention} set a slowmode delay of `{time}` in {channel.mention}", color=0x06c9ff)
        embed.set_author(name="Slow Mode")
        await ctx.send(embed=embed)

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

def setup(bot):
    bot.add_cog(SlowMode(bot))
