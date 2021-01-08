import discord

from .timedelta import format_time


class RoleResource:
    def __init__(self, ctx, role):
        self.ctx = ctx
        self.role = role

        self._get_role()

        if self.role is None:
            self.role = self.ctx.author.top_role

    def _get_role(self):
        """Fetch a role by its name."""

        if isinstance(self.role, discord.Role):
            return

        if self.role is None:
            return

        self.role = discord.utils.find(
            lambda r: r.name.lower().startswith(self.role.lower()), self.ctx.guild.roles
        )

    def role_embed(self):
        """Create an embed containing the role's information."""

        r: discord.Role = self.role

        rolecolor = str(r.color).upper()

        embed = discord.Embed(color=r.color)

        embed.set_author(name=f"Stats about {r.name}")

        embed.add_field(name="Role Name", value=f"{r.name}")
        embed.add_field(name="Color", value=rolecolor)
        embed.add_field(name="Members", value=len(r.members))
        embed.add_field(name="Created at", value=format_time(r.created_at))
        embed.add_field(name="Role Position", value=r.position)
        embed.add_field(name="Mention", value=r.mention)
        embed.add_field(name="Hoisted", value=r.hoist)
        embed.add_field(name="Mentionable", value=r.mentionable)
        embed.add_field(name="Managed", value=r.managed)

        embed.set_thumbnail(url=f"https://placehold.it/100/{str(rolecolor)[1:]}?text=+")
        embed.set_footer(text=f"Role ID: {r.id}")

        return embed
