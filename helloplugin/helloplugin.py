from discord.ext import commands
class HelloPlugin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if "hello" in message.content.startswith():
            await message.channel.send("Hey")
        elif "gm" in message.content.lower():
            await message.channel.send("Good Morning")
        elif "gn" in message.content.lower():
            await message.channel.send("Good Night")
        elif "good morning" in message.content.lower():
            await message.channel.send("Good Morning !")
        elif "good night" in message.content.lower():
            await message.channel.send("Good Night !")

def setup(bot):
    bot.add_cog(HelloPlugin(bot))
