import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes

class cSellDupes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="selldupes",
        description="Sell all your clothes dupes to earn Blings!",
    )           
    async def sell(
        self,
        inter: nextcord.Interaction,
        ):
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM obtained inner join clothes on (clothes.clothid = obtained.clothid) inner join outfits on (outfits.outfitid = clothes.outfitid) where userid = ? and guildid = ? and quantity > 1", (inter.user.id, inter.guild_id,))
            results = cur.fetchall()
            if (results == []):
                await inter.response.send_message(f'''You **don't own any dupe**! {emotes["emoteNikkiCry"]}''')
            else:
                sellDupesEmbed = nextcord.Embed()
                sellDupesEmbed.title = f'Dupes sold! {emotes["emoteNikkiWink"]}'
                sellDupesEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)

                totalQty = 0
                totalAmount = 0
                for item in results:
                    quantity = item[2]
                    clothid = item[4]
                    clothname = item[6]
                    outfitname = item[10]
                    outfitrarity = item[12]
                    
                    cur.execute("update obtained set quantity = 1 where userid = ? and clothid = ? and guildid = ?", (inter.user.id, clothid, inter.guild_id,))

                    cur.execute("select blings from users where userid = ? and guildid = ?", (inter.user.id, inter.guild_id,))
                    results = cur.fetchone()
                    blings = results[0] # blings de l'utilisateur
                    if int(outfitrarity) == 3:
                        totalAmount += 1500*(quantity-1)
                        cur.execute("update users set blings = ? where userid = ? and guildid = ?", (blings + 1500*(quantity-1), inter.user.id, inter.guild_id,))
                    elif int(outfitrarity) == 4:
                        totalAmount += 2500*(quantity-1)
                        cur.execute("update users set blings = ? where userid = ? and guildid = ?", (blings + 2500*(quantity-1), inter.user.id, inter.guild_id,))
                    else:
                        totalAmount += 5000*(quantity-1)
                        cur.execute("update users set blings = ? where userid = ? and guildid = ?", (blings + 5000*(quantity-1), inter.user.id, inter.guild_id,))
                    totalQty += quantity-1

                conn.commit()
                conn.close()

                sellDupesEmbed.add_field(name="Quantity of dupes sold", value=totalQty)
                sellDupesEmbed.add_field(name="Amount of Blings earned", value=f'{str(totalAmount)} {emotes["emoteBling"]}')
                sellDupesEmbed.add_field(name="Old balance", value=f'{str(blings)} {emotes["emoteBling"]}')
                sellDupesEmbed.add_field(name="New balance", value=f'{str(blings+totalAmount)} {emotes["emoteBling"]}')

                await inter.response.send_message(embed=sellDupesEmbed)
                    
        
def setup(bot: commands.Bot):
    bot.add_cog(cSellDupes(bot))