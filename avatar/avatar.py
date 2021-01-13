import discord 
import asyncio
from discord.ext import commands

class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def avatar(self, ctx, *, member : discord.Member = None):
        embed2 = discord.Embed(title=f"{member}'s Avatar!", color=0x00ff00)
        embed2.set_image(url==member.avatar_url)
        await ctx.send(embed=embed2)

def setup(bot):
    bot.add_cog(avatar(bot))
        
