import discord
from discord.ext import commands

class emoji(commands.Cog):
    """Reacts with a banana emoji if someone says banana."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'BANANA' in message.content.upper():
            await message.add_reaction('\N{BANANA}')
        elif 'APPLE' in message.content.upper():
            await message.add_reaction('\N{APPLE}')


def setup(bot):
    bot.add_cog(emoji(bot))
