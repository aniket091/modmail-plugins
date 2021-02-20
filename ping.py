from discord.ext import commands


class pingCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

@commands.command()
async def ping(self, ctx):
  await ctx.send("khoooool")

def setup(bot):
  bot.add_cog(ping(bot))
