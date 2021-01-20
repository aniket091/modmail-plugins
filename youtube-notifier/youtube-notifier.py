import asyncio, dateutil, discord, logging, os, random, typing

from discord.ext import commands
from core import checks
from core.models import PermissionLevel
from datetime import datetime

logger = logging.getLogger("Modmail")


class YoutubeNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.db = bot.plugin_db.get_partition(self)
        self.yt_channel = ""
        self.yt_playlist = ""
        self.discord_channel = ""
        self.enabled = True
        self.msg = ""
        self.icon = ""
        self.last_video = ""
        self.api_keys = list()
        self.bot.loop.create_task(self._set_db())

    async def _set_db(self):
        config = await self.db.find_one({"_id": "config"})
        if config is None:
            await self.db.find_one_and_update(
                {"_id": "config"},
                {
                    "$set": {
                        "yt": "",
                        "playlist": "",
                        "lastvideo": "",
                        "icon": "",
                        "message": "",
                        "channel": "",
                        "enabled": True,
                    }
                },
                upsert=True,
            )

        self.yt_channel = config.get("yt", "")
        self.yt_playlist = config.get("playlist", "")
        self.icon = config.get("icon", "")
        self.last_video = config.get("lastvideo", "")
        self.discord_channel = config.get("channel", "")
        self.msg = config.get("message", "")
        self.enabled = config.get("enabled", True)

        self.api_keys = os.getenv("YOUTUBE_KEYS", "").replace(" ", "").split(",")
        if len(self.api_keys) <= 0:
            logger.error("No API key found.")
            self.enabled = False
            return
        self.bot.loop.create_task(self._handle_notify(ch))

    async def _handle_notify(self, ch: typing.Optional[str]):
        while True:
            if not self.enabled or (
                self.yt_channel == ""
                or self.discord_channel == ""
                or self.yt_playlist == ""
            ):
                await asyncio.sleep(10)
            else:
                r = await self._check()
                if r["contentDetails"]["videoId"] == self.last_video:
                    await asyncio.sleep(10)
                    continue
                else:
                    channel = self.bot.get_channel(
                        ch if ch else int(self.discord_channel)
                    )
                    if channel is None:
                        await asyncio.sleep(10)
                        continue
                    url = f"youtube.com/watch?v={r['contentDetails']['videoId']}"
                    embed = discord.Embed(color=0xC4302B)
                    embed.description = r["snippet"]["description"]
                    embed.set_author(
                        r["snippet"]["channelTitle"],
                        url=f"https://youtube.com/channel/f{r['snippet']['channelId']}",
                    )
                    embed.title = r["snippet"]["title"]
                    embed.url = url
                    embed.description = r["snippet"]["description"].split("\n\n")[0]
                    embed.set_footer("Uploaded ")
                    embed.timestamp = dateutil.parser.parse("2019-12-31T17:05:00.000Z")
                    await channel.send(
                        f"{self.msg.replace('{url}', url) if len(self.msg) > 0 else ' '}",
                        embed=embed,
                    )
                    if ch:
                        return
                    else:
                        await asyncio.sleep(10)

    async def _check(self):
        try:
            resp = await self.bot.session.get(
                f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50"
                f"&playlistId={self.yt_playlist}&key={random.choice(self.api_keys)}",
                headers={"Accept": "application/json"},
            )

            json = resp.json()
            return json["items"][0]
        except Exception as e:
            logger.error(e)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def ytnotifier(self, ctx: commands.Context):
        """
        Manage youtube notifier settings
        """

        await ctx.send_help(ctx.command)
        return

    @ytnotifier.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def ytchannel(self, ctx: commands.Context, channelID: str):
        """
        Set the youtube channel ID
        """

        if len(self.api_keys) <= 0:
            logger.error("No API key found.")
            self.enabled = False
            return

        res = await self.bot.session.get(
            f"https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails&id={channelID}&key={random.choice(self.api_keys)}",
            headers={"Accept": "application/json"},
        )
        if res.status != 200:
            await ctx.send("Request failed")
            return
        json = await res.json()
        try:
            uploads = json["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            self.yt_playlist = uploads
            self.icon = json[0]["snippet"]["thumbnails"]["default"]["url"]
        except KeyError:
            await ctx.send("Failed. Check the ID Once")
            return
        except Exception as e:
            await ctx.send("Failed. Check Logs for more details")
            logger.error(e)
            return

        resp = await self.bot.session.get(
            f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={self.yt_playlist}&key={random.choice(self.api_keys)}",
            headers={"Accept": "application/json"},
        )
        if resp.status != 200:
            await ctx.send("Request failed")
            return
        json1 = await resp.json()
        try:
            last = json1["items"][0]["contentDetails"]["videoId"]
            self.last_video = last
        except KeyError:
            await ctx.send("Failed. Check the ID Once")
            return
        except Exception as e:
            await ctx.send("Failed. Check Logs for more details")
            logger.error(e)
            return

        await self.db.find_one_and_update(
            {"_id": "config"},
            {
                "$set": {
                    "yt": channelID,
                    "playlist": self.yt_playlist,
                    "lastvideo": self.last_video,
                    "icon": self.icon,
                    "updatedAt": datetime.utcnow(),
                }
            },
            upsert=True,
        )

        self.yt_channel = channelID
        await ctx.send("Done")
        return

    @ytnotifier.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Set the discord channel to sent the notification to
        """

        await self.db.find_one_and_update(
            {"_id": "config"},
            {"$set": {"channel": str(channel.id), "updatedAt": datetime.utcnow()}},
            upsert=True,
        )

        self.discord_channel = str(channel.id)
        await ctx.send("Done")
        return

    @ytnotifier.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def message(self, ctx: commands.Context, *, msg: str):
        await self.db.find_one_and_update(
            {"_id": "config"},
            {"$set": {"message": msg, "updatedAt": datetime.utcnow()}},
            upsert=True,
        )

        self.msg = msg
        await ctx.send("Done")

    @ytnotifier.command()
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def toggle(self, ctx: commands.Context):
        """
        Enable or disable notifications
        """
        await self.db.find_one_and_update(
            {"_id": "config"},
            {"$set": {"enabled": not self.enabled, "updatedAt": datetime.utcnow()}},
            upsert=True,
        )

        self.enabled = not self.enabled
        await ctx.send(f"{'Enabled' if self.enabled else 'Disabled'} the notifications")
        return


def setup(bot):
    bot.add_cog(YoutubeNotifier(bot))
