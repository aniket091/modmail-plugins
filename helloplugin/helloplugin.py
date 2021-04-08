from discord.ext import commands

class HelloPlugin(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot
        
   
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        if message.channel.id == 771389960468693062:
          return
        elif message.channel.id == 800775278603272212:
          return 
        elif message.channel.id == 716926336488177735:
          return     

        if message.guild.id == 791254312339898368:
          return   
        #hello
        if message.content.startswith("hello"): 
            await message.channel.send("Hello")
            await message.add_reaction("👋")
        elif message.content.startswith("Hello"):
            await message.channel.send("Hello !")
            await message.add_reaction("👋")
        elif message.content.startswith("HELLO"):
            await message.channel.send("hello")
            await message.add_reaction("👋")
        elif message.content.startswith("hemlo"):
            await message.channel.send("hello")
            await message.add_reaction("👋")    
         
         #hi   
        elif message.content.startswith("hi"):
            await message.channel.send("hi!")
            await message.add_reaction("✌️")
        elif message.content.startswith("Hi"):
            await message.channel.send("Hey!")
            await message.add_reaction("✌️")
        
         # good moring 🌅
        elif message.content.startswith("good morning"):
            await message.channel.send("Good Morning!")
            await message.add_reaction("🌅")
        elif message.content.startswith("Good morning"):
            await message.channel.send("Good Morning !")
        elif message.content.startswith("gm"):
            await message.channel.send("Good Morning!")
            await message.add_reaction("🌅")
        elif message.content.startswith("Gm"):
            await message.channel.send("Good Morning!")
        elif message.content.startswith("ji em"):
            await message.channel.send("Ji em vai!")
            await message.add_reaction("<:pranam:828272042402381844>")

         # goood night    🌃
        elif message.content.startswith("good night"):
            await message.channel.send("Good Night!")
            await message.add_reaction("🌃")
        elif message.content.startswith("Good night"):
            await message.channel.send("Good Night!") 
            await message.add_reaction("🌃")
        elif message.content.startswith("gn"):
            await message.channel.send("Good Night!")
            await message.add_reaction("🌃")
        elif message.content.startswith("Gn"):
            await message.channel.send("Good Night!")
            await message.add_reaction("🌃")
        elif message.content.startswith("ji en"):
            await message.channel.send("Ji en vai!")
            await message.add_reaction("<:pranam:828272042402381844>") 
        elif '<@!474255126228500480>' in message.content.lower():
            print("aniket")
            await message.add_reaction('<a:swag:791539777437433876>')     
        elif '<@!488738167969546272>' in message.content.lower():
            if message.guild.id == 665842728545943552:
                await message.add_reaction('<a:ohh:828312958769692692>')    
        elif '<@!686445028469768201>' in message.content.lower():
            if message.guild.id == 686445229687177228:
                await message.add_reaction('<a:ohh:828312958769692692>')  
        elif '<@!634028003114090526>' in message.content.lower():
            if message.guild.id == 686445229687177228:
                await message.add_reaction('<a:cookiee:829594080756498452>')          

def setup(bot):
    bot.add_cog(HelloPlugin(bot))
