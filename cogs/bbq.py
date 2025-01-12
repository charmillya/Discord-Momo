import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cBbq(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="bbq",
        description="Feed me some delicious BBQ!",
    )   
    async def bbq(self, inter: nextcord.Interaction):
        bbqEmbed = nextcord.Embed()
        bbqEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
        bbqEmbed.title = (f"BBQ fed!")
        bbqEmbed.set_thumbnail("https://cdn-icons-png.flaticon.com/512/7601/7601433.png")
        bbqEmbed.description = f'Thank you soooo much ehehe! *burp* {emotes["emoteNikkiWink"]}'
        await inter.response.send_message(embed = bbqEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cBbq(bot))