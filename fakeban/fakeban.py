import discord
from discord.ext import commands

class fakeBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = self.bot.main_color
        
    @commands.command(name="pban", aliases=['fban'])
    async def fban(self, ctx, member: discord.Member = None, reason = None):
        await ctx.message.delete()
        if not member:
            embed = discord.Embed(title="Error", description="Please provide a user to ban!", color=self.bot.error_color)
            await ctx.send(embed=embed)
        else:
            if not reason:
                embed = discord.Embed(title="Ban", description=f"{member.mention} Has been banned!", color=self.color)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Ban", description=f"{member.mention} Has been banned for {reason}!", color=self.color)
                await ctx.send(embed=embed)           
        
def setup(bot):
    bot.add_cog(fakeBan(bot))
