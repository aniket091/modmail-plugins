import discord
from discord.ext import commands

class edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command.command()
    async def edit(ctx, msg_id: int = None, channel: discord.TextChannel = None):
        if not msg_id:
            channel = client.get_channel(795002959392931870) # the message's channel
            msg_id = 797867472597811261 # the message's id
        elif not channel:
            channel = ctx.channel
        msg = await channel.fetch_message(msg_id)
        await msg.edit(content="Some content!")
        

def setup(bot):
    bot.add_cog(edit(bot))
