from discord.ext import commands
class HelloPlugin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.content.startswith("hello"):
            await message.channel.send("Hello !")
            await ctx.message.add_reaction("👋")
        elif message.content.startswith("Hello"):
            await message.channel.send("Hello !")
        elif message.content.startswith("HELLO"):
            await message.channel.send("Hello !")
        elif message.content.startswith("hi"):
            await message.channel.send("hello")
        elif message.content.startswith("Hi"):
            await message.channel.send("Hey !")
        elif message.content.startswith("good morning"):
            await message.channel.send("Good Morning !🌅")
        elif message.content.startswith("Good morning"):
            await message.channel.send("Good Morning !🌅")
        elif message.content.startswith("good night"):
            await message.channel.send("Good Night !🌃")
        elif message.content.startswith("Good night"):
            await message.channel.send("Good Night !🌃")
        elif message.content.startswith("gm"):
            await message.channel.send("Good Morning !🌅")
        elif message.content.startswith("Gm"):
            await message.channel.send("Good Morning !🌅")
        elif message.content.startswith("gn"):
            await message.channel.send("Good Night !🌃")
        elif message.content.startswith("Gn"):
            await message.channel.send("Good Night !🌃")

def setup(bot):
    bot.add_cog(HelloPlugin(bot))
