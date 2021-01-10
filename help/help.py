import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="***PARTH YT*** BOT COMMANDS!",
            description="aniket",
            color=0xee3463,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text="Management Team", icon_url="https://cdn.discordapp.com/attachments/726193232798810132/740629657191186562/7S-.gif")
        await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(help(bot))
