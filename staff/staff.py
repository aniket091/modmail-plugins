import asyncio

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.command()
    async def message(self, ctx):
        embed = discord.Embed(
            title="**Staff Status**"
            description="Online staff members"
            color="#009dff"
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text="Management Team")
        await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(staff(bot))        
