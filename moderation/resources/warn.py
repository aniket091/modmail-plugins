import discord
from datetime import datetime
from .util import Pag

class warnresource:
    def __init__(self, ctx, bot, db, channel, member):
        self.ctx = ctx
        self.db = db
        self.member =  member
        self.channel = channel
        self.bot = bot
        self.red = 0xfc4343
        self.green = 0x00ff5a
        self.yell = 0xfffc36
        self.tick = "<:tick:819613405597532160>"
        self.cross = "<:x2:819613332892942347>"


    async def warn(self, reason):
        member = self.member
        ctx = self.ctx
        if member == None:
            print("eror")
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}warn [member] [reason]\n**Example: **{ctx.prefix}warn @member doing spam!",
                color = self.red
            )
            return await ctx.send(embed = embed)

        if member.bot:
            return await ctx.send(embed=discord.Embed(
                description = f"**{self.cross} Bots can't be warned.**",
                color = self.red
            ))


        config = await self.db.find_one({"_id": "warns"})
        if config is None:
            config = await self.db.insert_one({"_id": "warns"})

        try:
            userwarns = config[str(member.id)]
        except KeyError:
            userwarns = config[str(member.id)] = []

        if userwarns is None:
            userw = []
        else:
            userw = userwarns.copy()

        timestamp = str(ctx.message.created_at.strftime("%b %d %Y"))
        case = await self.get_case()
        userw.append({"warn_id": str(case), "reason": reason, "mod_id": ctx.author.id, "timestamp": timestamp})
        
        await self.db.find_one_and_update(
            {"_id": "warns"}, {"$set": {str(member.id): userw}}, upsert=True
        )

        await ctx.send(embed = discord.Embed(
            description = f"{self.tick} **{member} has been warned!  || {reason}**",
            color = self.green
        ))
                        
        try:
            await member.send(embed=discord.Embed(
                description = f"**You have been warned in `{ctx.guild.name}`\n*Reason* : {reason}**",
                color = self.yell
            ))
        except discord.errors.Forbidden:
            return await self.channel.send(embed=await self.generateWarnEmbed(
                str(member.id), str(ctx.author.id), len(userw), reason, str("I could not DM them.")
            )) 

        await self.channel.send(
            embed = await self.generateWarnEmbed(
                str(member.id), str(ctx.author.id), len(userw), reason, str("y")
            )
        )    
        del userw
        return  

                   
    async def delwarn(self, num):
        member = self.member
        ctx = self.ctx
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}delwarn [member] [warn_id]\n**Example: **{ctx.prefix}delwarn @aniket 1",
                color = self.red
            )
            embed.set_footer(text="[] - Required")
            return await ctx.send(embed = embed)

        config = await self.db.find_one({"_id": "warns"})
        if config is None:
            return

        try:
            userwarns = config[str(member.id)]
        except KeyError:
            embed = discord.Embed(
                description = f"**{self.cross} No warnings found for {member.name}#{member.discriminator}**",
                color = self.red
            )
            return await ctx.send(embed = embed)

        if userwarns is None:
            embed = discord.Embed(
                description = f"**{self.cross} No warnings found for {member.name}#{member.discriminator}**",
                color = self.red
            )
            return await ctx.send(embed = embed)
        else:
            userw = userwarns.copy()
        
        final = ""
        for warn in userw:
            if warn['warn_id'] == num:
                final = "ok"
            else:
                if final == "ok":
                    final = "ok"
                else:
                    final = "no"              

        if final == "no":
            return  await ctx.send(embed = discord.Embed(
                description = f"**{self.cross} Please include a valid Warn ID**",
                color = self.red
            ))
        
        await self.db.update_one(
            { "_id": "warns" }, 
            { "$pull": { str(member.id): { 'warn_id': str(num) } } },
            upsert=True
        );

        
        await ctx.send(embed = discord.Embed(
            description = f"{self.tick} **Deleted warning with ID `{str(num)}` for {member.name}#{member.discriminator}**",
            color = self.green
        )) 
        embed  = discord.Embed(color = self.green, timestamp=datetime.utcnow())
        embed.set_author(name=f"Delete Warn 🗑️ | {member}", icon_url=member.avatar_url)
        embed.add_field(name="User", value=f"{member.mention}", inline=True)
        embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}", inline=True)
        embed.add_field(name="Warn ID", value=f"{str(num)}", inline=True)
        embed.add_field(name="Total Warns", value=f"{len(userw) - 1}", inline=True)
        embed.set_footer(text=f"ID: {member.id}")
        await self.channel.send(embed = embed)
       

    
    async def warns(self):
        member = self.member
        ctx = self.ctx 
        if member == None:
            embed = discord.Embed(
                title=f"{self.cross} Invalid Usage!",
                description = f"**Usage: **{ctx.prefix}warns [member]\n**Example: **{ctx.prefix}warns @aniket",
                color = self.red
            )
            await ctx.send(embed = embed)
            return
        
        config = await self.db.find_one({"_id": "warns"})
        if config is None:
            config = await self.db.insert_one({"_id": "warns"})

        try:
            userwarns = config[str(member.id)]
        except KeyError:
            embed = discord.Embed(
                description = f"**{self.cross} No warnings found for {member.name}#{member.discriminator}**",
                color = self.red
            )
            return await ctx.send(embed = embed)

        if userwarns is None:
            embed = discord.Embed(
                description = f"**{self.cross} No warnings found for {member.name}**",
                color = self.red
            )
            return await ctx.send(embed = embed)
        else:
            userw = userwarns.copy()

        #print(userw)  
        pages = [] 
        base = 0;
        description = "" 
        for warn in userw:
            base = base + 1
            description = f"""
            **Warn Number : `{base}`**
            **ID : **`{warn['warn_id']}`
            **Reason : **`{warn['reason']}`
            **Moderator : **<@{warn['mod_id']}>
            **Date : **`{warn['timestamp']}`\n
            """
            pages.append(description)
  
        num = len(userw) 
        embed = Pag(
            title = f"{num} Warns for {member.name}#{member.discriminator}",
            colour=0x4fc3f7,
            entries=pages,
            length=1
        )
        await embed.start(ctx)

    async def generateWarnEmbed(self, memberid, modid, warning, reason, status):
        member: discord.User = await self.bot.fetch_user(int(memberid))
        mod: discord.User = await self.bot.fetch_user(int(modid))

        embed = discord.Embed(color = self.yell, timestamp=datetime.utcnow())
        if warning == "0":
            data = "Pardon 🗑️"
        else:
            data = "Warn 📋"    
  
        embed.set_author( name=f"{data} | {member}", icon_url=member.avatar_url,)
        embed.add_field(name="User", value=f"<@{member.id}>", inline = True)
        embed.add_field(name="Moderator ", value=f"<@{modid}>", inline = True)
        if warning != "0":
            embed.add_field(name="Total Warns ", value=warning, inline = True)

        embed.add_field(name="Reason", value=reason, inline = True)
        embed.set_footer(text=f"ID: {member.id}")
        if status != "y":
            embed.add_field(name="Status ", value=status, inline=False)
        return embed

    async def get_case(self):
        """Gives the case number."""
        num = await self.db.find_one({"_id": "cases"})
        if num == None:
            num = 0
        elif "amount" in num:
            num = num["amount"]
            num = int(num)
        else:
            num = 0
        num += 1
        await self.db.find_one_and_update(
            {"_id": "cases"}, {"$set": {"amount": num}}, upsert=True
        )
        return f"{num}"            


        
        

