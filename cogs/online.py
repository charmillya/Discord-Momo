import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cOnline(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="online",
        description="Tests if I'm online!",
    )   
    async def online(self, inter: nextcord.Interaction) -> None:
        await inter.response.send_message(f'I am alive! {emotes["emoteNikkiKiss"]}')

        
def setup(bot: commands.Bot):
    bot.add_cog(cOnline(bot))