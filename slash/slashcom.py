import discord 
import asyncio
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

from random import randint
client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
guild_ids = [664505860327997461]

class slashcom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready():
        print("Ready!")
    @slash.slash(
      name="rps",
      description="TEST",
      options=[manage_commands.create_option(
        name = "rps",
        description = "play rps with bot",
        option_type = 3,
        required = True,
        choices =[
       {
         "name": "rock",
         "value": "rock"
       },{
         "name": "paper",
         "value": "paper"
       },{
         "name": "scissors",
         "value": "scissors"
       }]
      )],
    )

 

    async def _rps(ctx, rps: str):
      choicelist = ["rock", "paper", "scissors"]
      botval = choicelist[randint(0,2)]
      async def winner(bot,user):
        if(bot == 'scissors' and user == 'rock'):
         await ctx.send(f"bot choose {botval} you won")
        if(bot == 'rock' and user == 'paper'):
          await ctx.send(f"bot choose {botval} you won")
        if(bot == 'paper' and user == 'scissors'):
          await ctx.send(f"bot choose {botval} you won")
        if(bot == user):
          await ctx.send(f"BOT CHOOSE {botval} its a tie") 
        if(bot == 'rock' and user == 'scissors'):
          await ctx.send(f"bot choose {botval} you lost") 
        if(bot == 'paper' and user == 'rock'):
          await ctx.send(f"bot choose {botval} you lost") 
        if(bot == 'scissors' and user == 'paper'):
          await ctx.send(f"bot choose {botval} you lost") 
        await ctx.respond()
      await winner(botval,rps)



    @slash.slash(
      name="test",
      description="this returns the bot latency",
      options=[manage_commands.create_option(
        name = "title",
        description = "description of first argument",
        option_type = 3,
        required = True
      ),manage_commands.create_option(
        name = "content",
        description = "description of first argument",
        option_type = 3,
        required = True
      )],
      guild_ids=guild_ids
    )
    async def _test(ctx,content: str, title: str, color):
        embed = discord.Embed(title=f"{title}", description=f"{content}")
        await ctx.respond()
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(slashcom(bot))
