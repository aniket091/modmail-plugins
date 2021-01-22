import discord
from discord.ext import commands, tasks
import asyncio

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.first = None
        self.second = None
        self.third = None

    @tasks.loop(seconds=10)
    async def start_the_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ANIKET'S SERVER"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"?help"))
        await asyncio.sleep(10)
        server = self.bot.get_guild(800631529351938089)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{server.member_count} Members!"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"Modmail Threads!"))
        await asyncio.sleep(10)

    @commands.group(name="statusy", invoke_without_command=True)
    async def status_group(self, ctx):
        embed = discord.Embed(
            title="Change the Bot's Status!",
            description=f"Change the Bot's Status to make it change every 10 Seconds!\n\nAvailable Commands:\n`{self.bot.prefix}statusy start`: Start the Status Changing Process\n`{self.bot.prefix}statusy one`: Set the first status of the bot!\n`{self.bot.prefix}statusy two`: Set the second status of the bot!\n`{self.bot.prefix}statusy three`: Set third first status of the bot!",
            color=self.bot.main_color
        )
        await ctx.send(embed=embed)

    @status_group.command(name="start")
    async def statusy_start(self, ctx):
           self.start_the_status.start()
           await ctx.send("Done! If you experience any problems just run this command again!")

    
def setup(bot):
    bot.add_cog(Status(bot))
