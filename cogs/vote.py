import nextcord
import topgg
from nextcord.ext import commands
from assets.momoemotes import *

class cVote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="vote",
        description="Upvote me on top.gg to earn free rewards!",
    )   
    async def vote(
        self,
        inter: nextcord.Interaction,
        ):
        voteEmbed = nextcord.Embed()
        voteEmbed.title = f"Support me on top.gg! {emotes["emoteNikkiKiss"]}"
        voteEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        voteEmbed.description = f"[You can vote **here**](https://top.gg/bot/1326586963603619995/vote)!"
        voteEmbed.set_thumbnail(self.bot.user.avatar.url)
        voteEmbed.set_footer(text=f"Thank you so much! <3")
        await inter.response.send_message(embed=voteEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cVote(bot))