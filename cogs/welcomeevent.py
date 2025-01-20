import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cWelcomeEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if member.guild.id == 1323383627492364319:
            role = nextcord.utils.get(member.guild.roles, name="nikki's")
            channel = self.bot.get_channel(1323572410452017193)
            welcomeEmbed = nextcord.Embed()
            welcomeEmbed.title = f'Welcome, stylist {member.name}! {emotes["emoteNikkiKiss"]}'
            welcomeEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            welcomeEmbed.set_thumbnail('https://stickershop.line-scdn.net/stickershop/v1/product/28246239/LINEStorePC/main.png?v=1')
            welcomeEmbed.set_image(member.avatar.url)
            welcomeEmbed.description = f'''{member.mention}, I am __**Momo**__, yours truly **travel companion**! I invite you to wander through our different **discussion channels**, there are so many nice **nikki's** out there~ ! {emotes["emoteNikkiWink"]}'''
            await member.add_roles(role)
            await channel.send(embed=welcomeEmbed)

def setup(bot: commands.Bot):
    bot.add_cog(cWelcomeEvent(bot))