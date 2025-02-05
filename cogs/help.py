import nextcord
from nextcord.ext import commands
from assets.momoemotes import emotes

class cHelp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="help",
        description="Send all my commands in your DMs!",
    )   
        
    async def help(
        self,
        inter: nextcord.Interaction,
        ):
        helpEmbed = nextcord.Embed()
        helpEmbed.title = "Momo - Commands List :gear:"
        helpEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        helpEmbed.description = f'''

        __**Clothing {emotes["emoteWardrobe"]}:**__
        **/resonate**: Buy a random piece of clothing for 5,000 Blings!
        **/inventory**: Check your inventory!
        **/view**: Display information about a specified piece of clothing or outfit!
        **/dailyshop**: Display the daily clothes shop!
        **/sell**: Sell a piece of clothing of your choice to earn Blings!
        **/selldupes**: Sell all your clothes dupes to earn Blings!
        \n
        __**Mira Level {emotes["emoteMiraLevel"]}:**__
        **/miralevel**: Let you know your Mira Level and remaining Mira EXP before levelling up!
        **/leaderboard**: Check the 10 top stylists of the server!
        \n
        __**Blings {emotes["emoteBling"]}:**__
        **/blings**: Check your blings balance!
        \n
        __**Utility :bubbles::**__
        **/profile**: Display your MomoBot profile!
        **/birthdays**: List the 10 upcoming birthdays in the server!
        **/setbirthday**: Set your birthday to get a special gift on this day!
        **/guide**: Display a chosen Nikki guide!
        **/coinflip**: I flip a coin and tell you the result!
        \n
        __**Games :video_game::**__
        **/birthdays**: List the 10 upcoming birthdays in the server!
        **/guide**: Display a chosen Nikki guide!
        **/bbq**: Feed me some delicious BBQ!
        \n
        __**Miscellaneous :bangbang::**__
        **/daily**: Claim your daily random piece of clothing and/or Blings delivery!
        **/vote**: Upvote me on top.gg to earn free rewards!
        **/8ball**: I answer a question of yours!
        **/bbq**: Feed me some delicious BBQ!
        **/hug**: Hug up to 5 chosen stylists!
        **/code**: I send you a link to my GitHub code!

        '''
        try:
            await inter.user.send(embed=helpEmbed)
            await inter.response.send_message(f"Commands List sent! {emotes["emoteNikkiKiss"]}")
        except:
            await inter.response.send_message("My commands **didn't get to their destination**! :x: Try **turning ON** your DMs from anyone in **this server**!")

        
def setup(bot: commands.Bot):
    bot.add_cog(cHelp(bot))