import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cEcho(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="echo",
        description="I repeat what you say!",
    )  
    async def echo(self, interaction: nextcord.Interaction, arg: str):
        await interaction.response.send_message(f"You said: {arg}")

        
def setup(bot: commands.Bot):
    bot.add_cog(cEcho(bot))