# Custom changing status 
 
Set custom changing status for the bot!

# Status types 

 ##### Setting `Playing ` status
 await bot.change_presence(activity=discord.Game(name=f"{self.first/second/third}"))

 #### Setting `Streaming ` status
 await self.bot.change_presence(activity=discord.Streaming(name=f"{self.first/second/third}"))

 ### Setting `Listening ` status
 await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.first/second/third}"))

 ## Setting `Watching ` status
 await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.first/second/third}"))
