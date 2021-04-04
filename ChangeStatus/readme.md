# Custom changing status 
 
Set custom changing status for the bot!

# Status types 

 ## Setting **Playing** status
 __await bot.change_presence(activity=discord.Game(name=f"{status}"))__

 ### Setting **Streaming** status
 //await self.bot.change_presence(activity=discord.Streaming(name=f"{status}", url=""))

 ### Setting **Listening** status
 await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))

 ## Setting **Watching** status
 ||await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))||
