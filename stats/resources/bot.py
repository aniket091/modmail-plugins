import discord

from .timedelta import format_time


class BotResource:
    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot

    def bot_embed(self):
        """Create an embed containing the bot's information."""

        bot: discord.ext.commands.Bot = self.bot

        b: discord.Member = discord.utils.find(
            lambda m: m.id == self.bot.user.id, self.ctx.guild.members
        )

        embed = discord.Embed(color=b.color)

        embed.set_author(name=f"{b}'s Stats")

        embed.add_field(name="Prefix", value=f"`{bot.prefix}` or {b.mention}")
        embed.add_field(name="Latency", value=f"{bot.latency * 1000:.2f} ms")
        embed.add_field(name="Uptime", value=bot.uptime)
        embed.add_field(name="Created", value=format_time(b.created_at))

        embed.set_thumbnail(url=b.avatar_url)
        embed.set_footer(text=f"Bot ID: {b.id}")

        return embed
