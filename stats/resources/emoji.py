import discord

from .timedelta import format_time


class EmojiResource:
    def __init__(self, ctx, emoji, color):
        self.ctx = ctx
        self.emoji = emoji
        self.color = color

    def emoji_embed(self):
        """Create an embed containing the emoji's information."""

        e: discord.Emoji = self.emoji

        embed = discord.Embed(color=self.color)

        embed.set_author(name=f"{e.name.title()}'s Stats")

        embed.add_field(name="Created", value=format_time(e.created_at))
        embed.add_field(name="Guild Name", value=e.guild.name)
        embed.add_field(name="Guild ID", value=e.guild_id)
        embed.add_field(name="Animated", value=e.animated)
        embed.add_field(name="Managed", value=e.managed)

        embed.set_thumbnail(url=str(e.url))
        embed.set_footer(text=f"Emoji ID: {e.id}")

        return embed
