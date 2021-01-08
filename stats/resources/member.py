import discord

from .timedelta import format_time


class MemberResource:
    def __init__(self, ctx, member):
        self.ctx = ctx
        self.member = member

        self._get_member()
        if self.member is None:
            try:
                self.member = discord.utils.get(self.ctx.guild.members, id=int(self.ctx.channel.topic[9:]))
                if self.member is None:
                    self.member = self.ctx.author
            except (ValueError, TypeError):
                self.member = self.ctx.author

    def _get_member(self):
        """Fetch a member by its name or nickname."""

        if isinstance(self.member, discord.Member):
            return

        if self.member is None:
            self.member = None
            return

        for m in self.ctx.guild.members:
            if m.display_name.lower().startswith(self.member.lower()):
                self.member = m
                return

            if m.name.lower().startswith(self.member.lower()):
                self.member = m
                return

        self.member = None

    def member_embed(self):
        """Create an embed containing the member's information."""

        m: discord.Member = self.member

        # Find all of the roles a member has
        role_list = [
            role.mention
            for role in reversed(m.roles)
            if role is not self.ctx.guild.default_role
        ]

        
        join_position = sorted(m.guild.members, key=lambda m: m.joined_at).index(m) + 1

        embed = discord.Embed(color=m.color)

        embed.set_author(name=f"{str(m)}'s Stats")

        embed.add_field(name="Created", value=format_time(m.created_at))
        embed.add_field(name="Joined", value=format_time(m.joined_at))
        embed.add_field(name="Join Position", value=join_position)
        embed.add_field(name="Avatar URL", value=f"[Link]({m.avatar_url})")
        embed.add_field(name="Mention", value=m.mention)

        if m.activity is not None:
            activitytype = m.activity.type.name.title()
            activitytype += " to" if activitytype == "Listening" else ""

            embed.add_field(name="Activity", value=f"{activitytype} {m.activity.name}")

        embed.add_field(name="Status", value=m.status.name.title())
        embed.add_field(name="Nickname", value=m.nick)
        embed.add_field(name="Roles", value=" ".join(role_list))

        embed.set_thumbnail(url=m.avatar_url)
        embed.set_footer(text=f"User ID: {m.id}")

        return embed

    def avatar_embed(self):
        """Create an embed contain the member's avatar."""

        m: discord.Member = self.member

        embed = discord.Embed(color=m.color)

        embed.set_author(name=f"{str(m)}'s Avatar")

        embed.add_field(name="Avatar", value=f"[Link]({m.avatar_url})")

        embed.set_image(url=m.avatar_url)
        embed.set_footer(text=f"User ID: {m.id}")

        return embed

    def userstatus_embed(self):
        """Create an embed that shows the status of a member"""

        m: discord.Member = self.member
            
        statuses = ['online', 'idle', 'dnd', 'offline']
        colors = ["0x7ccca5","0xfca41b","0xf44444","0x9da4ad"]
        statuscolour = colors[statuses.index(m.status.name)]
        embed = discord.Embed(color=discord.Color(int(statuscolour,0)))
        images = ['https://cdn.discordapp.com/emojis/615846944341884948.png?v=1%27', 'https://cdn.discordapp.com/emojis/587932578221129748.png?v=1%27%22', 'https://cdn.discordapp.com/emojis/500353506474065920.png?v=1%27%22', 'https://cdn.discordapp.com/emojis/606534231492919312.png?v=1%27%22']
        embed.set_image(url=images[statuses.index(m.status.name)])
        embed.set_author(name=f"{str(m)}'s Status")
        embed.add_field(name='Status',value=m.status.name.title())
        embed.set_footer(text=f"User ID: {m.id}")

        return embed


    def join_embed(self):
        """Create an embed containing the member's join position."""

        m: discord.Member = self.member
        
        join_position = sorted(m.guild.members, key=lambda m: m.joined_at).index(m) + 1

        embed = discord.Embed(color=m.color)

        embed.set_author(name=f"{str(m)}'s Join Position")
        embed.add_field(name="Join Position", value=join_position)

        embed.set_thumbnail(url=m.avatar_url)
        embed.set_footer(text=f"User ID: {m.id}")

        return embed
