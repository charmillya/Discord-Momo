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
        description="Hug up to 5 chosen stylists!",
    )   
    async def hug(
        self,
        inter: nextcord.Interaction, 
        user: nextcord.Member = nextcord.SlashOption(
            required=True,
            name="stylist",
            description="The stylist you want to hug!"
        ),
        user2: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist_2",
            description="Another stylist you want to hug!"
        ),
        user3: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist_3",
            description="Another stylist you want to hug!"
        ),
        user4: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist_4",
            description="Another stylist you want to hug!"
        ),
        user5: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist_5",
            description="Another stylist you want to hug!"
        ),
        ):

        response = requests.get('https://api.any-bot.xyz/api/v1/hug')
        responseJSON = json.loads(response.text)

        hugEmbed = nextcord.Embed()
        if user2 or user3 or user4 or user5:
            allUsers = "" + user.display_name + " and "
            if user3:
                allUsers += user2.display_name + " and "
            else: 
                allUsers += user2.display_name
            if user4:
                allUsers += user3.display_name + " and "
            elif user3: 
                allUsers += user3.display_name
            if user5:
                allUsers += user4.display_name + " and"
                allUsers += user5.display_name
            elif user4: 
                allUsers += user4.display_name
        else:
            allUsers = user.display_name
        hugEmbed.title = f'''__{inter.user.display_name}__ hugs __{allUsers}__!'''
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