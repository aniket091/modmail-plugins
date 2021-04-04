import discord
from discord.ext import commands

class emoji(commands.Cog):
    """Reacts with a banana emoji if someone says banana."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if '<@!474255126228500480>' in message.content.lower():
            await message.add_reaction('<a:ohh:828312958769692692>')
        elif '<@!488738167969546272>' in message.content.lower() && message.guild.id == 665842728545943552:
            await message.add_reaction('<a:ohh:828312958769692692>')


def setup(bot):
    bot.add_cog(emoji(bot))
