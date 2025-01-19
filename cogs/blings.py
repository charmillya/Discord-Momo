import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes

class cBlings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="blings",
        description="Check your blings balance!",
    )   
    async def blings(
        self,
        inter: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist",
            description="View the blings balance of a specified stylist!"
        ),
        ):
        user = user or inter.user
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT blings FROM users WHERE userid = ?", (user.id,))
        results = cur.fetchone()
        conn.commit()
        conn.close()
        blingsEmbed = nextcord.Embed()
        blingsEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        blingsEmbed.title = (f"{user.name}'s Blings balance {emotes["emoteBling"]}")
        blingsEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/d/dd/Bling_Icon.png/revision/latest?cb=20241208230112")
        blingsEmbed.add_field(name=f'Blings', value=f'{str(results[0])} {emotes["emoteBling"]}')
        await inter.response.send_message(embed=blingsEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cBlings(bot))