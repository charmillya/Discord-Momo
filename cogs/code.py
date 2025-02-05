import nextcord
from nextcord.ext import commands

class cCode(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="code",
        description="I send you a link to my GitHub code!",
    )   
    async def code(
        self,
        inter: nextcord.Interaction,
        ):
        codeEmbed = nextcord.Embed()
        codeEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        codeEmbed.description = f"You can find my code **[here](https://github.com/charmillya/Discord-Momo)**!"
        await inter.response.send_message(embed=codeEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cCode(bot))