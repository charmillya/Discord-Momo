import nextcord
import sqlite3
from datetime import datetime
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cDaily(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="daily",
        description="Claim your daily random piece of clothing!",
    )           
    async def daily(
        self,
        inter: nextcord.Interaction
        ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT lastdaily FROM users WHERE userid = ?", (inter.user.id,))
        results = cur.fetchone()
        lastDaily = results[0]
        currDate = datetime.today().strftime('%Y-%m-%d')
        if currDate != lastDaily:
            cur.execute("SELECT COUNT(clothname) FROM clothes")
            results = cur.fetchone()
            nbClothes = results[0]
            cur.execute("SELECT COUNT(userid) FROM obtained WHERE userid = ?", (inter.user.id,))
            results = cur.fetchone()
            if nbClothes > results[0]:
                obtainedUserID = inter.user.id
                while ((obtainedUserID == inter.user.id)):
                    cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, obtained.userid, obtained.clothid, outfits.outfitrarity FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) LEFT OUTER JOIN obtained ON (obtained.clothid = clothes.clothid) LEFT OUTER JOIN USERS ON (users.userid = obtained.userid) ORDER BY RANDOM() LIMIT 1")
                    results = cur.fetchone()
                    selectedClothID = results[1]
                    obtainedUserID = results[4]
                    if obtainedUserID != inter.user.id:
                        cur.execute("SELECT * FROM obtained WHERE userid = ? and clothid = ?", (inter.user.id, selectedClothID,))
                        results2 = cur.fetchone()
                        if results2 == None:
                            break
                        else:
                            obtainedUserID = inter.user.id
                cur.execute("INSERT INTO obtained VALUES (?, ?)", (inter.user.id, selectedClothID,))
                cur.execute("UPDATE users SET lastdaily = ? WHERE userid = ?", (currDate, inter.user.id,))
                conn.commit()
                conn.close()
                dailyEmbed = nextcord.Embed()
                if results[6] == 3:
                    dailyEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif results[6] == 4:
                    dailyEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    dailyEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                dailyEmbed.title = (f"Your daily free piece of clothing {emotes["emoteWardrobe"]}")
                dailyEmbed.description = "The following piece of clothing has been added to your inventory!"
                dailyEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                dailyEmbed.add_field(name="Outfit", value=f'{str((results[0]))}')
                dailyEmbed.add_field(name="Name", value=f"{str(results[2])}")
                dailyEmbed.add_field(name="Rarity", value=f"{str(results[6])}  {emotes['emoteStar']}")
                dailyEmbed.set_image(results[3])
                await inter.response.send_message(embed = dailyEmbed)
            else:
                await inter.response.send_message("You've already collected all pieces of clothing!")
        else:
            await inter.response.send_message(f'''You've **already obtained** your daily free piece of clothing! Come back **tomorrow**! {emotes["emoteNikkiWink"]}''')
        
def setup(bot: commands.Bot):
    bot.add_cog(cDaily(bot))