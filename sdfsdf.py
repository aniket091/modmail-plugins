@commands.command(aliases=["f"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def offline(self, ctx, *, msgID: str):
        """End a training."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed2=discord.Embed(description=f"{ctx.author.mention}\n**__Status__**\n**Offline** <:dnd:797692836745183232>", color=0xFF0000, timestamp=datetime.datetime.utcnow())
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await message.edit(embed=embed2, content=training_mention) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-42 <:dnd:797692836745183232>")
        await asyncio.sleep(60)
        await message.delete()
        
    @commands.command(aliases=["10-7"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def tenseven(self, ctx, *, msgID: str):
        """break for staff."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed3=discord.Embed(description=f"{ctx.author.mention}\n**__Status__**\n**Break (10-7)** <:idle:797695058207178753>", color=0xFFFF00)
        await message.edit(embed=embed3) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting 10-7 <:idle:797695058207178753>")
        
    @commands.command(aliases=["10-8"])
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    async def teneight(self, ctx, *, msgID: str):
        """back for staff."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try: 
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed=discord.Embed(title="Please include a valid Message ID that is in the training channel.", description="[Where can I find a Message ID?](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xe74c3c)
            await ctx.send(embed=embed)
        embed4=discord.Embed(description=f"{ctx.author.mention}\n**__Status__**\n**Back (10-8)** <:streaming:798080684778061835>", color=0x9900cc)
        await message.edit(embed=embed4) # <@&695243187043696650>
        
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention}, reporting back 10-8 <:streaming:798080684778061835><:online:797692836911906816>")


            
def setup(bot):
    bot.add_cog(staff(bot))
