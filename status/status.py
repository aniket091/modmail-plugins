import discord
import asyncio
from discord.ext import commands, tasks

class utility(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        self.statuss.start()
    

    @tasks.loop(seconds=10)
    async def statuss(self):
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ANIKET'S SERVER"))  
      await asyncio.sleep(10)
      await self.bot.change_presence(activity=discord.Activity(type=discord.Game, name=f"Message me for help!"))
      await asyncio.sleep(10)
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"!help"))
      await asyncio.sleep(10)
      server = self.bot.get_guild(800631529351938089)  #parth's server
      await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{server.member_count} Members!"))
      await asyncio.sleep(10)

    @statuss.before_loop
    async def before_statuss(self):
      await self.bot.wait_until_ready()  

def setup(bot):
    bot.add_cog(utility(bot))
