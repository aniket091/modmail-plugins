import discord

from .timedelta import format_time


class GuildResource:
    def __init__(self, ctx, color):
        self.ctx = ctx
        self.guild = self.ctx.guild
        self.color = color

    def guild_embed(self):
        """Create an embed containing the guild's information."""

        g: discord.Guild = self.guild

        bots = len([m for m in g.members if m.bot])
        humans = len([m for m in g.members if not m.bot])
        animated = len([m for m in g.emojis if m.animated])
        normal = len([m for m in g.emojis if not m.animated])

        embed = discord.Embed(title="🖥️ SERVER INFORMATION 🖥️", color=self.color)


        embed.add_field(name="Server name", value=f"```{g.name}```")
        embed.add_field(name="Server owner", value=f"```{g.owner.name}```")
        embed.add_field(name=f"Server members [{g.member_count}]", value=f"```Members: {humans} | Bots: {bots}```", inline=False)
        embed.add_field(name="Server ID", value=f"```{g.id}```")
        embed.add_field(name="Server Region", value=f"```{g.region.name.title()}```")
        num = len(g.channels) + len(g.categories)
        embed.add_field(
            name=f"Server categories and channels [{num}]", 
            value=f"```Categories: {len(g.categories)} | Text: {len(g.text_channels)} | Voice: {len(g.voice_channels)}```",
            inline = False
        )
        embed.add_field(name=f"Server emojis [{len(g.emojis)}]", value=f"```Normal: {normal} | Animated: {animated}```", inline = False)
        embed.add_field(name="Server created on (MM/DD/YYYY)", value=f"```{format_time(g.created_at)}```", inline=False)

        embed.set_thumbnail(url=str(g.icon_url))

        return embed
