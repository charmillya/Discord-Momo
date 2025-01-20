import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cLeaveEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        if member.guild.id == 1323383627492364319:
            channel = self.bot.get_channel(1323572410452017193)
            welcomeEmbed = nextcord.Embed()
            welcomeEmbed.title = f'Farewell, stylist {member.name}! {emotes["emoteNikkiCry"]}'
            welcomeEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            welcomeEmbed.set_image(member.avatar.url)
            welcomeEmbed.description = f'I hope that we will cross paths again .. {emotes["emoteNikkiCry"]}'
            await channel.send(embed=welcomeEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(cLeaveEvent(bot))