from discord.ext import commands
import discord
import asyncio
import datetime

from core import checks
from core.models import PermissionLevel


def to_emoji(c):
    base = 0x1F1E6
    return chr(base + c)


class Polls(commands.Cog):
    """Poll voting system."""

    def __init__(self, bot):
        self.ctx = ctx
        self.bot = bot

    @commands.group(name="poll", invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def poll(self, ctx: commands.Context):
        """📊 Easily create Polls."""
        await ctx.send_help(ctx.command)

    @poll.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def start(self, ctx, *, question):
        """Interactively creates a poll with the following question.
        To vote, use reactions!
        """
        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.add_reactions:
            return await ctx.send("Need Add Reactions permissions.")

        # a list of messages to delete when we're all done
        messages = [ctx.message]
        answers = []

        def check(m):
            return (
                m.author == ctx.author
                and m.channel == ctx.channel
                and len(m.content) <= 100
            )

        for i in range(20):
            messages.append(
                await ctx.send(
                    f"Say a Poll option or {ctx.prefix}done to publish the Poll."
                )
            )

            try:
                entry = await self.bot.wait_for("message", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f"{ctx.prefix}done"):
                break

            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass  # oh well
        
        nickn = ctx.author.nick 
        if nickn == None:
            nickn = ctx.author.name

        answer = "\n\n".join(f"{keycap}  **{content}**" for keycap, content in answers)
        embed = discord.Embed(
            color=0x4fc3f7,
            title=f"📊 {question}",
            description=f"{answer}",
        )
        b: discord.Member = discord.utils.find(
            lambda m: m.id == self.bot.user.id, self.ctx.guild.members
        ) 
        embed.set_author(name="Poll !", icon_url=b.avatar_url)
        embed.set_footer(text=f"Created by {nickn}", icon_url=ctx.author.avatar_url)
        poll = await ctx.send(embed=embed)
        for emoji, _ in answers:
            await poll.add_reaction(emoji)

    @start.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("Missing the question.")

    @poll.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def quick(self, ctx, *questions_and_choices: str):
        """
        Makes a poll quickly!
        **The first argument is the `question` and the rest are the `choices` !**
        
        **Example: ** `?poll quick "Green or Light Green!" Green "Light Green"`

        **It can be a simple yes or no poll !**
        **Example: ** `?poll quick "Do you watch Anime?"`
        """

        if len(questions_and_choices) == 0:
            return await ctx.send("You need to specify a question.")
        elif len(questions_and_choices) == 2:
            return await ctx.send("You need at least 2 choices.")
        elif len(questions_and_choices) > 21:
            return await ctx.send("You can only have up to 20 choices.")

        perms = ctx.channel.permissions_for(ctx.me)
        if not perms.add_reactions:
            return await ctx.send("Need Add Reactions permissions.")
        try:
            await ctx.message.delete()
        except:
            pass
        question = questions_and_choices[0]

        if len(questions_and_choices) == 1:
            embed = discord.Embed(
                color=0x4fc3f7, description=f"**{question}**"
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            poll = await ctx.send(embed=embed)
            reactions = ["👍", "👎"]
            for emoji in reactions:
                await poll.add_reaction(emoji)

        else:
            choices = [
                (to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])
            ]
            nickn = ctx.author.nick 
            if nickn == None:
                nickn = ctx.author.name

            body = "\n\n".join(f"{key}  **{c}**" for key, c in choices)
            embed = discord.Embed(
                color=0x4fc3f7,
                title=f"📊 {question}",
                description=f"{body}",
            )
            b: discord.Member = discord.utils.find(
                lambda m: m.id == self.bot.user.id, self.ctx.guild.members
            ) 
            embed.set_author(name="Poll !", icon_url=b.avatar_url)
            embed.set_footer(text=f"Created by {nickn}", icon_url=ctx.author.avatar_url)
            poll = await ctx.send(embed=embed)
            for emoji, _ in choices:
                await poll.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Polls(bot))
