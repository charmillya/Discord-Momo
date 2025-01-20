import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes

class cPull(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="pull",
        description="Buy a random piece of clothing for 5,000 Blings!",
    )   
    async def pull(
        self,
        inter: nextcord.Interaction
    ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(clothname) FROM clothes")
        results = cur.fetchone()
        nbClothes = results[0]
        cur.execute("SELECT COUNT(obtained.userid) FROM obtained WHERE obtained.userid = ? AND obtained.guildid = ?", (inter.user.id, inter.guild_id,))
        results = cur.fetchone()
        if nbClothes > results[0]:
            cur.execute("SELECT blings FROM users WHERE userid = ? AND guildid = ?", (inter.user.id, inter.guild_id))
            results = cur.fetchone()
            userBalance = results[0]
            if userBalance - 5000 >= 0:
                cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, outfits.outfitrarity FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) ORDER BY RANDOM() LIMIT 1")
                results = cur.fetchone()
                outfitname = results[0]
                selectedClothID = results[1]
                clothname = results[2]
                clothimage = results[3]
                outfitrarity = results[4]
                cur.execute("SELECT clothid, quantity FROM obtained WHERE clothid = ? AND guildid = ?", (selectedClothID, inter.guild_id,))
                results = cur.fetchone()
                if results != None:
                    quantity = results[1]
                else:
                    quantity = 1
                cur.execute("INSERT INTO obtained VALUES (?, ?, ?, ?)", (inter.user.id, selectedClothID, quantity, inter.guild_id))
                cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (userBalance-5000, inter.user.id, inter.guild_id,))
                pullEmbed = nextcord.Embed()
                if outfitrarity == 3:
                    pullEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    pullEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    pullEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                pullEmbed.title = (f"Your obtained piece of clothing {emotes["emoteWardrobe"]}")
                pullEmbed.description = "The following piece of clothing has been added to your inventory:"
                pullEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                pullEmbed.set_image(clothimage)
                pullEmbed.add_field(name="Outfit", value=f'{str((outfitname))}')
                pullEmbed.add_field(name="Name", value=f"{str(clothname)}")
                pullEmbed.add_field(name="Rarity", value=f"{str(outfitrarity)}  {emotes['emoteStar']}")
                cur.execute("SELECT blings FROM users WHERE userid = ? AND guildid = ?", (inter.user.id, inter.guild_id,))
                results = cur.fetchone()
                conn.commit()
                conn.close()
                pullEmbed.add_field(name="New balance", value=f"{results[0]} {emotes['emoteBling']}")
                await inter.response.send_message(embed = pullEmbed)
            else:
                await inter.response.send_message(f'''You don't have **enough Blings** {emotes["emoteBling"]} ! Your current balance : **{userBalance}** {emotes["emoteBling"]}''')
        else:
            await inter.response.send_message("You've already collected all pieces of clothing!")

def setup(bot: commands.Bot):
    bot.add_cog(cPull(bot))