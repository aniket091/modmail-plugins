import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class avatar(commands.Cog):
    """
    gives you the avatar of the person
    """
    
    @commands.command()
async def avatar(self, ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
    
    def setup(bot):
    bot.add_cog(avatar(bot))
