import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes

class cSell(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="sell",
        description="Sell a piece of clothing of your choice to earn Blings!",
    )           
    async def sell(
        self,
        inter: nextcord.Interaction,
        item: str = nextcord.SlashOption(
            name="item",
            description="The piece of clothing you want to sell!"
        ),
        ):
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT clothes.clothid, clothes.clothname, clothes.clothimage, outfits.outfitname, outfits.outfitrarity FROM obtained INNER JOIN clothes ON (clothes.clothid = obtained.clothid) LEFT OUTER JOIN outfits ON (outfits.outfitid = clothes.outfitid) WHERE obtained.userid = ? AND clothes.clothname = ? AND obtained.guildid = ?", (inter.user.id, item, inter.guild_id,))
            results = cur.fetchone()
            if (results is None):
                await inter.response.send_message(f'''You either gave me an **incorrect item name**, or you **don't own** it! {emotes["emoteNikkiCry"]}''')
            else:
                clothid = results[0]
                clothname = results[1]
                clothimage = results[2]
                outfitname = results[3]
                outfitrarity = results[4]

                async def yes_callback(interaction):
                    nonlocal sent_msg
                    noButton.disabled = True
                    yesButton.disabled = True
                    cur.execute("DELETE FROM obtained WHERE obtained.userid = ? AND clothid = ? AND obtained.guildid = ?", (inter.user.id, clothid, inter.guild_id,))
                    cur.execute("SELECT blings FROM users WHERE userid = ? AND guildid = ?", (inter.user.id, inter.guild_id,))
                    results = cur.fetchone()
                    userBlings = results[0]
                    if outfitrarity == 3:
                        cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (userBlings+1500, inter.user.id, inter.guild_id,))
                    elif outfitrarity == 4:
                        cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (userBlings+3500, inter.user.id, inter.guild_id,))
                    else:
                        cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (userBlings+5000, inter.user.id, inter.guild_id,))
                    conn.commit()
                    conn.close()
                    sellEmbed = nextcord.Embed()
                    sellEmbed.title = (f"Piece of clothing sold! {emotes["emoteNikkiKiss"]}")
                    sellEmbed.description = f'You sold the following piece of clothing:'
                    if outfitrarity == 3:
                        sellEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                    elif outfitrarity == 4:
                        sellEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                    else:
                        sellEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                    sellEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                    sellEmbed.add_field(name="Outfit", value=f'{outfitname}')
                    sellEmbed.add_field(name="Name", value=f"{clothname}")
                    sellEmbed.add_field(name="Rarity", value=f"{outfitrarity} {emotes["emoteStar"]}")
                    sellEmbed.add_field(name="Old balance", value=f"{userBlings} {emotes["emoteBling"]}")
                    if outfitrarity == 3:
                        sellEmbed.add_field(name="New balance", value=f"{userBlings+1500} {emotes["emoteBling"]}")
                    elif outfitrarity == 4:
                        sellEmbed.add_field(name="New balance", value=f"{userBlings+3500} {emotes["emoteBling"]}")
                    else:
                        sellEmbed.add_field(name="New balance", value=f"{userBlings+5000} {emotes["emoteBling"]}")
                    sellEmbed.set_image(clothimage)
                    await inter.edit_original_message(embed=sellEmbed, view=myview)

                async def no_callback(interaction):
                    nonlocal sent_msg
                    noButton.disabled = True
                    yesButton.disabled = True
                    cancelledEmbed = nextcord.Embed()
                    cancelledEmbed.title = (f"Cancelled successfully! {emotes["emoteNikkiWink"]}")
                    cancelledEmbed.description = f'No worries, you kept your item!'
                    cancelledEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                    cancelledEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                    await inter.edit_original_message(embed=cancelledEmbed, view=myview)

                sellEmbed = nextcord.Embed()
                sellEmbed.title = (f"Selling confirmation :bangbang:")
                sellEmbed.description = f'Are you sure that you want to sell the following piece of clothing ?'
                if outfitrarity == 3:
                    sellEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    sellEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    sellEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                sellEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                sellEmbed.add_field(name="Outfit", value=f'{outfitname}')
                sellEmbed.add_field(name="Name", value=f"{clothname}")
                sellEmbed.add_field(name="Rarity", value=f"{outfitrarity} {emotes["emoteStar"]}")
                sellEmbed.set_image(clothimage)
                yesButton = Button(label="Yes!", style=ButtonStyle.blurple)
                yesButton.callback = yes_callback # next_callback : retour programme quand on appuie sur yes
                noButton = Button(label="No..", style=ButtonStyle.blurple)
                noButton.callback = no_callback # next_callback : retour programme quand on appuie sur yes
                myview = View(timeout=180)
                myview.add_item(yesButton)
                myview.add_item(noButton)
                sent_msg = await inter.response.send_message(embed=sellEmbed, view=myview)
        
def setup(bot: commands.Bot):
    bot.add_cog(cSell(bot))