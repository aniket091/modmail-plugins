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
        
        if e.animated == "False":
            animate = "❌ No"
        else:
            animate = "✔️ Yes"

        embed = discord.Embed(title=":laughing: EMOJI INFORMATION :laughing:", color=self.color)
        embed.add_field(name="Emoji Name", value=f"```{e.name.title()}```")
        embed.add_field(name="Emoji ID", value=f"```{e.id}```")
        embed.add_field(name="Is animated", value=f"```{animate}```")
        embed.add_field(name="Emoji URL", value=f"Open it in your browser [click here]({str(e.url)}).")
        embed.add_field(name="Emoji created on (MM/DD/YYYY)", value=f"```{format_time(e.created_at)}```", inline = False) 

        embed.set_thumbnail(url=str(e.url))

        return embed
