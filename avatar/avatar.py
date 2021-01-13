import discord 
import asyncio
from discord.ext import commands

class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def avatar(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        m: discord.Member = self.member
        embed = discord.Embed(title=f"{str(m)}'s Avatar!", color=0x00ff00)
        embed2.set_image(url=m.avatar_url)
        await ctx.send(embed=embed2)

def setup(bot):
    bot.add_cog(avatar(bot))
        
