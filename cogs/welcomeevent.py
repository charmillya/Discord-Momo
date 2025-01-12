import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cWelcomeEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        welcomeChannel = commands.Bot.fetch_channel(1323572410452017193)
        await ctx.channel.send("hello")

def setup(bot: commands.Bot):
    bot.add_cog(cWelcomeEvent(bot))