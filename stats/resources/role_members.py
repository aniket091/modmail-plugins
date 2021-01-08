import discord

from .timedelta import format_time


class RoleMembersResource:
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

    def role_members_embed(self):
        """Create an embed containing the role members."""

        r: discord.Role = self.role

        member_list = r.members.copy()

        embeds = [
            discord.Embed(
                title=f"Members in {discord.utils.escape_markdown(r.name).title()}",
                color=r.color,
                description="",
            ).set_thumbnail(url=f"https://placehold.it/100/{str(r.color)[1:]}?text=+")
        ]
        entries = 0

        if member_list:
            embed = embeds[0]

            for m in sorted(member_list, key=lambda m: m.name.lower()):
                line = f"{m.name}#{m.discriminator}\n"
                if entries == 25:
                    embed = discord.Embed(
                        title=f"Members in {r.name.title()} (Continued)",
                        color=r.color,
                        description=line,
                    ).set_thumbnail(
                        url=f"https://placehold.it/100/{str(r.color)[1:]}?text=+"
                    )
                    embeds.append(embed)
                    entries = 1
                else:
                    embed.description += line
                    entries += 1
        else:
            embeds[0].description = "Currently there are no members in that role."

        return embeds
