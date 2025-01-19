import nextcord
import random
from nextcord.ext import commands
from time import sleep
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cCoinFlip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="coinflip",
        description="I flip a coin and tell you the result!",
    )   
    async def view(
        self,
        inter: nextcord.Interaction,
        ):
        answers = ["Heads!", "Tails!"]
        waitEmbed = nextcord.Embed()
        waitEmbed.title = "Flipping a coin .. :coin:"
        waitEmbed.description = "Wait a little bit .. (it's just to add suspense)"
        waitEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        await inter.response.send_message(embed=waitEmbed)
        choice = random.choice(answers)
        randEmbed = nextcord.Embed()
        randEmbed.title = "Coin flip! :coin:"
        randEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        randEmbed.add_field(name="The coin landed on ... :drum:", value=f'**{choice}**')
        if choice == "Heads!":
            randEmbed.set_image("https://freepngimg.com/save/26113-euro-coin-transparent-background/2400x2400")
        else:
            randEmbed.set_image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/LV_2_eiro.png/602px-LV_2_eiro.png")
        sleep(4)
        await inter.edit_original_message(embed=randEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cCoinFlip(bot))