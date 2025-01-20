import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes

class cGive(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="give",
        description="Give a piece of clothing of your choice to another stylist!",
    )           
    async def give(
        self,
        inter: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            name="stylist",
            description="The stylist you want to donate to!"
        ),
        item: str = nextcord.SlashOption(
            name="item",
            description="The piece of clothing you want to donate!"
        ),
        ):
        if inter.user.id == user.id:
            await inter.response.send_message(f'Hey dummy! You cannot give an item to **yourself**! {emotes["emoteNikkiWink"]}')
        else:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT clothes.clothid, clothes.clothname, clothes.clothimage, outfits.outfitname, outfits.outfitrarity FROM obtained INNER JOIN clothes ON (clothes.clothid = obtained.clothid) LEFT OUTER JOIN outfits ON (outfits.outfitid = clothes.outfitid) INNER JOIN users ON (obtained.userid = users.userid) WHERE obtained.userid = ? AND clothes.clothname = ? AND obtained.guildid = ?", (inter.user.id, item, inter.guild_id,))
            results = cur.fetchone()
            if (results is None):
                await inter.response.send_message(f'''You either gave me an **incorrect item name**, or you **don't own** it! {emotes["emoteNikkiCry"]}''')
                conn.commit()
                conn.close()
            else:
                clothid = results[0]
                clothname = results[1]
                clothimage = results[2]
                outfitname = results[3]
                outfitrarity = results[4]

                async def no_callback(interaction):
                    nonlocal sent_msg
                    noButton.disabled = True
                    yesButton.disabled = True
                    cancelledEmbed = nextcord.Embed()
                    cancelledEmbed.title = (f"Cancelled successfully! {emotes["emoteNikkiWink"]}")
                    cancelledEmbed.description = f'No worries, you kept your item!'
                    cancelledEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                    cancelledEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                    conn.commit()
                    conn.close()
                    await inter.edit_original_message(embed=cancelledEmbed, view=myview)

                async def yes_callback(interaction):
                    nonlocal sent_msg
                    noButton.disabled = True
                    yesButton.disabled = True
                    conn = sqlite3.connect('momodb.db')
                    cur = conn.cursor()
                    cur.execute("SELECT * FROM obtained WHERE obtained.userid = ? AND clothid = ? AND obtained.guildid = ?", (user.id, clothid, inter.guild_id,))
                    results = cur.fetchone()
                    if results is None:
                        cur.execute("INSERT INTO obtained VALUES (?, ?, ?)", (user.id, clothid, inter.guild_id))
                        cur.execute("DELETE FROM obtained WHERE userid = ? AND clothid = ? AND guildid = ?", (inter.user.id, clothid, inter.guild_id,))
                        conn.commit()
                        conn.close()
                        giveEmbed = nextcord.Embed()
                        if outfitrarity == 3:
                            giveEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                        elif outfitrarity == 4:
                            giveEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                        else:
                            giveEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                        giveEmbed.title = (f"Piece of clothing given! {emotes["emoteNikkiKiss"]}")
                        giveEmbed.description = f'{user.mention}, {inter.user.mention} gave you the following piece of clothing:'
                        giveEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                        giveEmbed.add_field(name="Outfit", value=f'{outfitname}')
                        giveEmbed.add_field(name="Name", value=f"{clothname}")
                        giveEmbed.add_field(name="Rarity", value=f"{outfitrarity} {emotes["emoteStar"]}")
                        giveEmbed.set_image(clothimage)
                        await inter.edit_original_message(embed=giveEmbed, view=myview)
                    else:
                        conn.commit()
                        conn.close()
                        await inter.response.send_message(f'The stylist you want to give that piece of clothing to **already owns it**! {emotes["emoteNikkiCry"]}')

                giveEmbed = nextcord.Embed()
                giveEmbed.title = (f"Giving confirmation :bangbang:")
                giveEmbed.description = f'Are you sure that you want to give the following piece of clothing ?'
                if outfitrarity == 3:
                    giveEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    giveEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    giveEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                giveEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                giveEmbed.add_field(name="Outfit", value=f'{outfitname}')
                giveEmbed.add_field(name="Name", value=f"{clothname}")
                giveEmbed.add_field(name="Rarity", value=f"{outfitrarity} {emotes["emoteStar"]}")
                yesButton = Button(label="Yes!", style=ButtonStyle.blurple)
                yesButton.callback = yes_callback # next_callback : retour programme quand on appuie sur yes
                noButton = Button(label="No..", style=ButtonStyle.blurple)
                noButton.callback = no_callback # next_callback : retour programme quand on appuie sur yes
                myview = View(timeout=180)
                myview.add_item(yesButton)
                myview.add_item(noButton)
                sent_msg = await inter.response.send_message(embed = giveEmbed, view=myview)
        
def setup(bot: commands.Bot):
    bot.add_cog(cGive(bot))