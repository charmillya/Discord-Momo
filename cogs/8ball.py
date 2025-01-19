import nextcord
import random
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class c8Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="8ball",
        description="I answer a question of yours!",
    )   
    async def view(
        self,
        inter: nextcord.Interaction,
        name: str = nextcord.SlashOption(
            name="question",
            description="The question you want me to answer to!"
        ),
        ):
        answers = ["For sure!", "I don't know..", "I wouldn't bet on it!", ":zzz:", "Erm.. please seek help! :heart:", "Hold on you're so right??", "Never ever!", "No, really not..", "YESSS YOU GET IT", "Why even?", "I prefer BBQ..", 
           "Please stop bothering me with that..", "Hear me out..", "I don't really see the point?", "YESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYESYES",
           "NONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONONO"]
        ballEmbed = nextcord.Embed()
        ballEmbed.title = "8ball! :8ball:"
        ballEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        ballEmbed.add_field(name="Your question:", value=f'{name}')
        ballEmbed.add_field(name="My answer:", value=random.choice(answers))
        ballEmbed.set_thumbnail("https://discord.com/assets/4aae9b932841972e89af.svg")
        await inter.response.send_message(embed=ballEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(c8Ball(bot))