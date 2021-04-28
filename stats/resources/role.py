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

        if r.hoist == "True":
            hoist = "✔️ Yes"
        else:    
            hoist = "❌ No"

        embed = discord.Embed(title=":construction_worker: ROLE INFORMATION :construction_worker:", color=r.color)

        embed.add_field(name="Role Name", value=f"```{r.name}```")
        embed.add_field(name="Role ID", value=f"```{r.id}```")

        embed.add_field(name="Hoisted", value=f"```{hoist}```", inline=False)
        embed.add_field(name="Members", value=f"```{len(r.members)}```")
        embed.add_field(name="Role Position", value=f"```{r.position}```")
        embed.add_field(name="Color", value=f"```{rolecolor}```")

        embed.add_field(name="Role created on (MM/DD/YYYY)", value=f"```{format_time(r.created_at)}```")
        
        embed.set_thumbnail(url=f"https://placehold.it/100/{str(rolecolor)[1:]}?text=+")


        return embed
