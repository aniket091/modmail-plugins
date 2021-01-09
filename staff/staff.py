import discord
from discord.ext import commands

class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def send_s(self, ctx):
        embed = discord.Embed(
            title="***7 SIN'S SOCIALS***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            description="<:instagram:724501733317017682> **Instagram:**\n• <https://www.instagram.com/7sinsggs/>\n\n<:youtube:663247076167122945> **YouTube:**\n• <https://www.youtube.com/channel/UCrA0fNlbVXKoA1eSu8YsYhA/featured>\n\n<:twitter:724501698248441877> **Twitter:**\n• <https://twitter.com/7sinsGGs>\n\n<:twitch:740634096446734366> **Twitch:**\n• <https://www.twitch.tv/7sinsggs>",
            color=0xee3463,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text="Management Team", icon_url="https://cdn.discordapp.com/attachments/726193232798810132/740629657191186562/7S-.gif")
        await ctx.send(embed=embed)
        
        @commands.command()
        async def online(self, ctx, member : discord.Member):
            await ctx.send(f"{member} reporting 10-41")
        
def setup(bot):
    bot.add_cog(staff(bot))
