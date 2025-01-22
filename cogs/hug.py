import nextcord
import requests
import json
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cHug(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="hug",
        description="Hug a chosen stylist!",
    )   
    async def hug(
        self,
        inter: nextcord.Interaction, 
        user: nextcord.Member = nextcord.SlashOption(
            required=True,
            name="stylist",
            description="The stylist you want to hug!"
        ),
        ):

        response = requests.get('https://api.any-bot.xyz/api/v1/hug')
        responseJSON = json.loads(response.text)

        hugEmbed = nextcord.Embed()
        hugEmbed.title = f'''__{inter.user.display_name}__ hugs __{user.display_name}__!'''
        hugEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        hugEmbed.set_image(responseJSON["image"])

        if user.id == inter.user.id:
            hugEmbed.title = f'''__{self.bot.user.display_name}__ hugs __{user.display_name}__!'''
            hugEmbed.description = f'You cannot **hug yourself**, dummy! However .. **I can**! {emotes["emoteNikkiKiss"]}'
        
        if user.id == self.bot.user.id:
            hugEmbed.description = f'I love you too! {emotes["emoteNikkiKiss"]}'

        await inter.response.send_message(embed=hugEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(cHug(bot))