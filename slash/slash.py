
import discord
import inspect
import typing
from discord.ext import commands
from .utils import manage_commands
from .model import CogCommandObject, CogSubcommandObject

from random import randint
client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
guild_ids = [664505860327997461]

class slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content="Pong!")


def setup(bot):
    bot.add_cog(slash(bot))
