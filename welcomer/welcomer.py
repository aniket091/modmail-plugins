import json

import discord
from box import Box
from discord.ext import commands

from .models import apply_vars, SafeString


class Welcomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.invite_cache = {}
        bot.loop.create_task(self.populate_invite_cache())

    async def populate_invite_cache(self):
        await self.bot.wait_until_ready()
        for g in self.bot.guilds:
            self.invite_cache[g.id] = {i for i in await g.invites()}

    async def get_used_invite(self, guild):
        """Checks which invite is used in join via the following strategies:
        1. Check if invite doesn't exist anymore
        2. Check invite uses
        """
        update_invite_cache = {i for i in await guild.invites()}

        for i in self.invite_cache[guild.id]:
            if i in update_invite_cache:
                # pass check 1
                try:
                    new_invite = next(inv for inv in update_invite_cache if inv.id == inv.id)
                except StopIteration:
                    continue
                else:
                    if new_invite.uses > i.uses:
                        return new_invite
        return Box(default_box=True, default_box_attr='{unable to get invite}')

    def apply_vars_dict(self, member, message, invite):
        for k, v in message.items():
            if isinstance(v, dict):
                message[k] = self.apply_vars_dict(member, v, invite)
            elif isinstance(v, str):
                message[k] = apply_vars(self, member, v, invite)
            elif isinstance(v, list):
                message[k] = [self.apply_vars_dict(member, _v, invite) for _v in v]
            if k == 'timestamp':
                message[k] = v[:-1]
        return message

    def format_message(self, member, message, invite):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            # message is not embed
            message = apply_vars(self, member, message, invite)
            message = {'content': message}
        else:
            # message is embed
            message = self.apply_vars_dict(member, message, invite)

            if any(i in message for i in ('embed', 'content')):
                message['embed'] = discord.Embed.from_dict(message['embed'])
            else:
                message = None
        return message

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def welcomer(self, ctx, channel: discord.TextChannel, *, message):
        """Sets up welcome command.
        """
        # Example usage: `welcomer #general`
        # """
        if message.startswith('https://') or message.startswith('http://'):
            # message is a URL
            if message.startswith('https://hastebin.cc/'):
                message = 'https://hastebin.cc/raw/' + message.split('/')[-1]

            async with self.bot.session.get(message) as resp:
                message = await resp.text(encoding='utf8')

        formatted_message = self.format_message(ctx.author, message, SafeString('{invite}'))
        if formatted_message:
            await channel.send(**formatted_message)
            await self.db.find_one_and_update(
                {'_id': 'config'},
                {'$set': {'welcomer': {'channel': str(channel.id), 'message': message}}},
                upsert=True
            )
            await ctx.send(f'Message sent to {channel.mention} for testing.\nNote: invites cannot be rendered in test message')
        else:
            await ctx.send('Invalid welcome message syntax.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        invite = await self.get_used_invite(member.guild)
        config = (await self.db.find_one({'_id': 'config'}))['welcomer']
        if config:
            channel = member.guild.get_channel(int(config['channel']))
            if channel:
                embed=discord.Embed(description="<:xRGB_logo2:827129630435573770> Welcome {member.mention}, Welcome To XRGB Server.")
                embed.set_image(url=member.avatar_url)
                embed.set_author(name=member,url=member.avatar_url,icon_url=member.avatar_url)
                embed.set_footer(text="Welcome To XRGB Server",icon_url=member.avatar_url)
                embed.add_field(name="<a:xRGB_Diamond:836677944487313479> Make Sure To Check These Channels", value="<a:xRGB_cube:740438963474530354> <#704493672309194822>", inline=True)
                embed.add_field(name="<a:xRGB_Diamond:836677944487313479> Make Sure To Join Us In", value="<a:xRGB_cube:740438963474530354> <#638162275945152515>", inline=True)
                channel.send(embed)

                


def setup(bot):
    bot.add_cog(Welcomer(bot))
