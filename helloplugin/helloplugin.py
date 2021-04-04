from discord.ext import commands
from pymongo.collection import Collection
from core import checks
from core.models import PermissionLevel, getLogger
import discord

class HelloPlugin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
        self.db: Collection = bot.plugin_db.get_partition(self)
        self.channel_blacklist: list = list()
        self.bot.loop.create_task(self._set_val())
    
    async def _update_db(self):
        await self.db.find_one_and_update(
            {"_id": "config"},
            {
                "$set": {
                    "blacklist": {
                        "channel": self.channel_blacklist,
                    },
                }
            },
            upsert=True,
        )

    async def _set_val(self):
        config = await self.db.find_one({"_id": "config"})

        if config is None:
            await self._update_db()
            return
        
        self.channel_blacklist = config["blacklist"]["channel"]    

    @checks.has_permissions(PermissionLevel.MOD)
    @commands.group(invoke_without_command=True)
    async def hellopmod(self, ctx: commands.Context):
        """Lets you blacklist channels for hello plugin!"""
        await ctx.send_help(ctx.command)
    
    @hellopmod.command(name="channel")
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def blacklist_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Blacklist Channels so that hello plugin message dont appear in the channels
        **Usage:**
        starboard blacklist channel **#channel**
        """
        if str(channel.id) in self.channel_blacklist:
            self.channel_blacklist.remove(str(channel.id))
            await self._update_db()
            removed = True
        else:
            self.channel_blacklist.append(str(channel.id))
            await self._update_db()
            removed = False

        await ctx.send(f"{'Un' if removed else None}Blacklisted {channel.mention}")
        return

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        if self.channel_blacklist.__contains__(str(message.channel_id)):
            return

        #hello
        if message.content.startswith("hello"): 
            await message.channel.send("Hello")
            await message.add_reaction("👋")
        elif message.content.startswith("Hello"):
            await message.channel.send("Hello !")
            await message.add_reaction("👋")
        elif message.content.startswith("HELLO"):
            await message.channel.send("hello")
            await message.add_reaction("👋")
         
         #hi   
        elif message.content.startswith("hi"):
            await message.channel.send("hi!")
            await message.add_reaction("✌️")
        elif message.content.startswith("Hi"):
            await message.channel.send("Hey!")
            await message.add_reaction("✌️")
        
         # good moring 🌅
        elif message.content.startswith("good morning"):
            await message.channel.send("Good Morning!")
            await message.add_reaction("🌅")
        elif message.content.startswith("Good morning"):
            await message.channel.send("Good Morning !")
        elif message.content.startswith("gm"):
            await message.channel.send("Good Morning !")
            await message.add_reaction("🌅")
        elif message.content.startswith("Gm"):
            await message.channel.send("Good Morning !")
        elif message.content.startswith("ji em"):
            await message.channel.send("Ji em vai !")
            await message.add_reaction("<:pranam:828272042402381844>")

         # goood night    🌃
        elif message.content.startswith("good night"):
            await message.channel.send("Good Night !")
            await message.add_reaction("🌃")
        elif message.content.startswith("Good night"):
            await message.channel.send("Good Night !") 
            await message.add_reaction("🌃")
        elif message.content.startswith("gn"):
            await message.channel.send("Good Night !")
            await message.add_reaction("🌃")
        elif message.content.startswith("Gn"):
            await message.channel.send("Good Night !")
            await message.add_reaction("🌃")


def setup(bot):
    bot.add_cog(HelloPlugin(bot))
