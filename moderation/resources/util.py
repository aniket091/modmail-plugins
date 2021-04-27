import asyncio

import discord
from discord.ext import buttons


class Pag(buttons.Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

