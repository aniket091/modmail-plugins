from typing import Optional

import discord
from discord.ext import commands
from nekosbest import Client


class Action(commands.Cog):
    """
    Action commands!
    """

    def __init__(self, bot):
        self.bot = bot
        self.client = Client()

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def kiss(self, ctx: commands.Context, user: discord.Member):
        """Kiss a user!"""

        author = ctx.author
        result = await self.client.get_image("kiss")

        if user == self.bot.user:
            msg = f"*OwO! kisses {author.mention} back!*"
            return await ctx.reply(msg)

        if user is not ctx.author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} kisses {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "Congratulations, you kissed yourself! LOL!!!"
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def pat(self, ctx: commands.Context, user: discord.Member):
        """Pats a user!"""

        author = ctx.author
        result = await self.client.get_image("pat")

        if user == self.bot.user:
            msg = "Thanks for the pats, I guess."
            return await ctx.reply(msg)

        if user is not author:
            msg = f"> *{author.mention} pats {user.mention}*"
        else:
            msg = f"> *{author.mention} pats themselves, I guess?*"
        embed = discord.Embed(colour=user.color)
        embed.set_image(url=result.url)
        await ctx.send(content=msg, embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def hug(self, ctx: commands.Context, user: discord.Member):
        """hug a user!"""

        author = ctx.author
        result = await self.client.get_image("hug")
        if user == self.bot.user:
            msg = f"Awwww thanks! So nice of you! *hugs {author.mention} back*"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} hugs {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "One dOEs NOt SiMplY hUg THeIR oWn sELF!"
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def slap(self, ctx: commands.Context, user: discord.Member):
        """Slaps a user!"""

        author = ctx.author
        result = await self.client.get_image("slap")

        if user == self.bot.user:
            msg = "**Ｎ Ｏ   Ｕ**"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} slaps {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "Don't slap yourself, you're precious!"
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def baka(self, ctx: commands.Context, user: discord.Member):
        """Call a user BAKA with a GIF reaction!"""

        author = ctx.author
        result = await self.client.get_image("baka")

        if user == self.bot.user:
            msg = "**Ｎ Ｏ   Ｕ**"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} calls {user.mention} a BAKA bahahahahaha*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "You really are BAKA, stupid."
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def tickle(self, ctx: commands.Context, user: discord.Member):
        """Tickles a user!"""

        author = ctx.author
        result = await self.client.get_image("tickle")

        if user == self.bot.user:
            msg = f"LMAO. Tickling a bot now, are we? {author.mention}"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} tickles {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "Tickling yourself is boring!"
            msg += " Tickling others is more fun though."
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def smug(self, ctx: commands.Context, user: Optional[discord.Member] = None):
        """Be smug towards someone!"""

        author = ctx.author
        result = await self.client.get_image("smug")

        embed = discord.Embed(colour=author.colour)
        if not user:
            msg = f"> *{author.mention} smugs at @\u200bsomeone*"
        else:
            user = user[0]
            msg = f"> *{author.mention} smugs at {user.mention}*"
        embed.set_image(url=result.url)
        await ctx.send(content=msg, embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def cuddle(self, ctx: commands.Context, user: discord.Member):
        """Cuddles a user!"""

        author = ctx.author
        result = await self.client.get_image("cuddle")
        if user == self.bot.user:
            return await ctx.reply("Come come. We'll cuddle all day and night!")
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} cuddles {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "Cuddling yourself sounds like a gay move LMFAO!"
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def poke(self, ctx: commands.Context, user: discord.Member):
        """Pokes a user!"""

        author = ctx.author
        result = await self.client.get_image("poke")

        if user == self.bot.user:
            msg = f"Awwww! Hey there. *pokes {author.mention} back!*"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} casually pokes {user.mention}*"
            embed.set_image(url=result.url)
            return await ctx.send(content=msg, embed=embed)
        else:
            msg = "Self-poking is widely regarded as a bad move!"
            await ctx.reply(msg)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def feed(self, ctx: commands.Context, user: discord.Member):
        """Feeds a user!"""

        author = ctx.author
        result = await self.client.get_image("feed")

        if user == self.bot.user:
            msg = f"OWO! Yummy food! Thanks {author.mention} :heart:"
            return await ctx.reply(msg)
        if user is not author:
            embed = discord.Embed(colour=user.colour)
            msg = f"> *{author.mention} feeds {user.mention}*"
            embed.set_image(url=result.url)
            await ctx.send(content=msg, embed=embed)
        else:
            msg = "Congrats you just fed yourself."
            await ctx.reply(msg)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(embed_links=True)
    async def cry(self, ctx: commands.Context):
        """Let others know you feel like crying or just wanna cry."""

        author = ctx.author
        result = await self.client.get_image("cry")
        embed = discord.Embed(colour=author.colour)
        embed.description = f"{author.mention} is crying"
        embed.set_image(url=result.url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Action(bot))
