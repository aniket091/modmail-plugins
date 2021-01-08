import typing
import datetime
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.paginator import EmbedPaginatorSession

from .resources.bot import BotResource
from .resources.emoji import EmojiResource
from .resources.guild import GuildResource
from .resources.member import MemberResource
from .resources.role_members import RoleMembersResource
from .resources.role import RoleResource


class Stats(commands.Cog):
    """Get useful stats about a member, the Modmail bot or your server"""

    def __init__(self, bot):
        self.bot = bot

    # Stats Group
    @commands.group(name="stats", aliases=["stat"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats(self, ctx):
        """Stats"""

        await ctx.send_help(ctx.command)

    # All Stats

    @stats.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def all(self, ctx):
        """Sends all stats embeds at once."""

        embeds = []

        embeds.append(MemberResource(ctx, None).avatar_embed())
        embeds.append(BotResource(ctx, self.bot).bot_embed())
        embeds.append(GuildResource(ctx, self.bot.main_color).guild_embed())
        embeds.append(MemberResource(ctx, None).member_embed())
        embeds.append(RoleResource(ctx, None).role_embed())

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()

    # Avatar

    @commands.command(aliases=["avatarinfo"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def avatar(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        """Get the avatar of a member."""

        embed = MemberResource(ctx, member).avatar_embed()
        await ctx.send(embed=embed)

    @stats.command(name="avatar")
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_avatar(
        self, ctx, *, member: typing.Union[discord.Member, str] = None
    ):
        """Get the avatar of a member."""

        await ctx.invoke(self.bot.get_command("avatar"), member=member)

    # Bot

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def botinfo(self, ctx):
        """Get the stats of your Modmail bot."""

        embed = BotResource(ctx, self.bot).bot_embed()
        await ctx.send(embed=embed)

    @stats.command(name="bot")
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_bot(self, ctx):
        """Get the stats of your Modmail bot."""

        await ctx.invoke(self.bot.get_command("botinfo"))

    # Emoji

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def emoji(self, ctx, *, emoji: discord.Emoji):
        """Get the stats of an emoji."""

        embed = EmojiResource(ctx, emoji, self.bot.main_color).emoji_embed()
        await ctx.send(embed=embed)

    @stats.command(name="emoji")
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_emoji(self, ctx, *, emoji: discord.Emoji):
        """Get the stats of an emoji."""

        await ctx.invoke(self.bot.get_command("emoji"), emoji=emoji)

    # Member

    @commands.command(aliases=["memberinfo", "user", "userinfo"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def member(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        """Get the stats of a member."""

        embed = MemberResource(ctx, member).member_embed()
        await ctx.send(embed=embed)

    @stats.command(name="member", aliases=["user"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_member(
        self, ctx, *, member: typing.Union[discord.Member, str] = None
    ):
        """Get the stats of a member."""

        await ctx.invoke(self.bot.get_command("member"), member=member)

    # Role Members

    @commands.command(aliases=["rolemembers"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def members(self, ctx, *, role: typing.Union[discord.Role, str] = None):
        """Get info about a role"""

        embeds = RoleMembersResource(ctx, role).role_members_embed()

        session = EmbedPaginatorSession(ctx, *embeds)
        await session.run()

    # Role

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def roleinfo(self, ctx, *, role: typing.Union[discord.Role, str] = None):
        """Get the stats of a role."""

        embed = RoleResource(ctx, role).role_embed()
        await ctx.send(embed=embed)

    @stats.command(name="role")
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_role(self, ctx, *, role: typing.Union[discord.Role, str] = None):
        """Get the stats of a role."""

        await ctx.invoke(self.bot.get_command("roleinfo"), role=role)

    # Server

    @commands.command(aliases=["guild", "guildinfo", "serverinfo"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def server(self, ctx):
        """Get the stats of your server"""

        embed = GuildResource(ctx, self.bot.main_color).guild_embed()
        await ctx.send(embed=embed)

    @stats.command(name="server", aliases=["guild"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def stats_server(self, ctx):
        """Get the stats of your server"""

        await ctx.invoke(self.bot.get_command("server"))

    # Status

    @commands.command(aliases=["us"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def userstatus(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        """Get the status of a member."""

        embed = MemberResource(ctx, member).userstatus_embed()
        await ctx.send(embed=embed)

# Join 

    @commands.command(aliases=["jp"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def joinposition(self, ctx, *, member: typing.Union[discord.Member, str] = None):
        """Get the join position of a member."""

        embed = MemberResource(ctx, member).join_embed()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))
