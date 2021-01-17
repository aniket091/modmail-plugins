from discord.ext import commands
class HelloPlugin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.content.startswith("hello"):
            await message.channel.send("Hello whats up")

def setup(bot):
    bot.add_cog(HelloPlugin(bot))
