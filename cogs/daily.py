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
        description="Claim your daily random piece of clothing and Blings delivery!",
    )           
    async def daily(
        self,
        inter: nextcord.Interaction,
        type: int = nextcord.SlashOption(
            name="type",
            choices={"Pull": 1, "Blings": 2},
        ),
        ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        if type == 1:
            cur.execute("SELECT lastdailypull FROM users WHERE userid = ? AND guildid = ?", (inter.user.id, inter.guild_id,))
            results = cur.fetchone()
            lastDailyPull = results[0]
            currDate = datetime.today().strftime('%Y-%m-%d')
            if currDate != lastDailyPull:
                cur.execute("SELECT COUNT(clothname) FROM clothes")
                results = cur.fetchone()
                nbClothes = results[0]
                cur.execute("SELECT COUNT(obtained.userid) FROM obtained WHERE obtained.userid = ? AND obtained.guildid = ?", (inter.user.id, inter.guild_id,))
                results = cur.fetchone()
                if nbClothes > results[0]:
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
                    cur.execute("INSERT INTO obtained VALUES (?, ?, ?, ?)", (inter.user.id, selectedClothID, quantity, inter.guild_id,))
                    cur.execute("UPDATE users SET lastdailypull = ? WHERE userid = ? AND guildid = ?", (currDate, inter.user.id, inter.guild_id,))
                    conn.commit()
                    conn.close()
                    dailyEmbed = nextcord.Embed()
                    if outfitrarity == 3:
                        dailyEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                    elif outfitrarity == 4:
                        dailyEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                    else:
                        dailyEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                    dailyEmbed.title = (f"Your daily free piece of clothing {emotes["emoteWardrobe"]}")
                    dailyEmbed.description = "The following piece of clothing has been added to your inventory:"
                    dailyEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                    dailyEmbed.add_field(name="Outfit", value=f'{str((outfitname))}')
                    dailyEmbed.add_field(name="Name", value=f"{str(clothname)}")
                    dailyEmbed.add_field(name="Rarity", value=f"{str(outfitrarity)}  {emotes['emoteStar']}")
                    dailyEmbed.set_image(clothimage)
                    await inter.response.send_message(embed = dailyEmbed)
                else:
                    await inter.response.send_message("You've already collected all pieces of clothing!")
            else:
                await inter.response.send_message(f'''You've **already obtained** your daily free piece of clothing! Come back **tomorrow**! {emotes["emoteNikkiWink"]}''')
        else:
            cur.execute("SELECT blings, lastdailyblings FROM users WHERE userid = ? AND guildid = ?", (inter.user.id, inter.guild_id,))
            results = cur.fetchone()
            userBlings = results[0]
            lastDailyBlings = results[1]
            currDate = datetime.today().strftime('%Y-%m-%d')
            if currDate != lastDailyBlings:
                cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (userBlings+3000, inter.user.id, inter.guild_id,))
                cur.execute("UPDATE users SET lastdailyblings = ? WHERE userid = ? AND guildid = ?", (currDate, inter.user.id, inter.guild_id,))
                conn.commit()
                conn.close()
                dailyEmbed = nextcord.Embed()
                dailyEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                dailyEmbed.title = (f"Your daily Blings delivery! {emotes["emoteBling"]}")
                dailyEmbed.description = "Your Blings balance has been succesfully incremented:"
                dailyEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/d/dd/Bling_Icon.png/revision/latest?cb=20241208230112")
                dailyEmbed.add_field(name="Old balance", value=f'{userBlings}')
                dailyEmbed.add_field(name="New balance", value=f"{userBlings+3000}")
                await inter.response.send_message(embed = dailyEmbed)
            else:
                await inter.response.send_message(f'''You've **already obtained** your daily Blings delivery! Come back **tomorrow**! {emotes["emoteNikkiWink"]}''')

        
def setup(bot: commands.Bot):
    bot.add_cog(cDaily(bot))