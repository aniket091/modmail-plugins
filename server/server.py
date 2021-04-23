import discord
import asyncio
from datetime import datetime
from discord.ext import commands, tasks
import psutil
from core import checks
from core.models import PermissionLevel

class Server(commands.Cog):  
    def __init__(self, bot):
      self.bot = bot
      self.db = bot.plugin_db.get_partition(self)
      self.channel = None
      self.msg = None
      self.serverr.start()
    
    async def _update_db(self):
      await self.db.find_one_and_update(
          {"_id": "config"},
          {
              "$set": {
                  "channel": self.channel,
                  "message": self.msg,
              }
          },
          upsert=True,
      ) 

    @tasks.loop(seconds=4)
    async def serverr(self):
      config = await self.db.find_one({"_id": "config"})
      if not config:
        print("no config")
        return
      
      cchannel = self.bot.get_channel(
        int(config["channel"])
      )

      message = await cchannel.fetch_message(
        int(config["message"])
      )    
      
      # embed op or wat?
      embed = discord.Embed(color = 0x3cfa5f, timestamp=datetime.utcnow(), title="Server Stats")
      desc = "```Elm"     
      desc += f"\nCPU: Intel(R) Xeon(R) CPU E5-2670 v2 (2.50GHz)\nCPU Usage: {psutil.cpu_percent()}% \n\n"
      desc += f"Cores (Physical): {psutil.cpu_count(logical=False)} \nCores (Total): {psutil.cpu_count(logical=True)}"
      desc += "\n------------------------------------- \nTotal Devices: 3\n\n"
      desc += f"Memory Usage (w/ buffers): {round(psutil.virtual_memory().used /1024/1024/1024, 2)} GB/{round(psutil.virtual_memory().total /1024/1024/1024, 2)} GB \nAvailable: {round(psutil.virtual_memory().available /1024/1024/1024, 2)} GB"
      desc += "\n-------------------------------------"
      desc += f"\nDisk Usage: {round(psutil.disk_usage('/').used /1024/1024/1024, 2)} GB/{round(psutil.disk_usage('/').total /1024/1024/1024, 2)} GB"
      desc += "\n------------------------------------- \nNetwork Stats: \n\n"
      desc += f"Current Transfer: {round(psutil.net_io_counters().bytes_sent / 1000, 2)} KB/s \nCurrent Received: {round(psutil.net_io_counters().bytes_recv / 1000, 2)} KB/s"
      desc += "\n-------------------------------------"
      desc += f"\nUptime: {self.bot.uptime}```"
      embed.add_field(name="Server Info", value=desc, inline=False)
      m = "```arm"
      m += f"\n {round(self.bot.latency * 1000)} ms```"
      embed.add_field(name="Discord API websocket ping", value=m, inline=False)
      embed.set_footer(text="Updated at") 

      await message.edit(embed = embed)


    @serverr.before_loop
    async def before_serverr(self):
      await self.bot.wait_until_ready() 

    
    @checks.has_permissions(PermissionLevel.OWNER) 
    @commands.command() 
    async def scc(self, ctx, msgID : int):
      if msgID == None:
        return await ctx.send_help(ctx.command)

      try:
        message = await ctx.fetch_message(msgID)
        if message:
          msgid = msgID
          channel = ctx.message.channel
      except:
        embed=discord.Embed(description="**Please include a valid message ID!**", color=self.ercolor)    
        await ctx.send(embed=embed, delete_after = 10.0)    
      
      self.channel = str(channel.id)
      self.msg = str(msgid)
      await self._update_db()
      await ctx.send(f"Done! {channel.mention} is the Channel now!")   

def setup(bot):
  bot.add_cog(Server(bot))
