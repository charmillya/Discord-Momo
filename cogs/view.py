import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cView(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="view",
        description="Display information about a specified piece of clothing or outfit!",
    )   
    async def view(
        self,
        inter: nextcord.Interaction,
        type: int = nextcord.SlashOption(
            name="type",
            choices={"Item": 1, "Outfit": 2},
        ),
        name: str = nextcord.SlashOption(
            name="name",
            description="The name of the piece of clothing / outfit you want to display!"
        ),
        ):
        if type == 1:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT clothes.clothid, clothes.clothname, clothes.clothimage, outfits.outfitname, outfits.outfitrarity FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) WHERE clothname = ?", (name,))
            results = cur.fetchone()
            if (results is None):
                await inter.response.send_message(f'''You either gave me an **incorrect item name**, or it **doesn't exist**! {emotes["emoteNikkiCry"]}''')
            else:
                clothname = results[1]
                clothimage = results[2]
                outfitname = results[3]
                outfitrarity = results[4]
                conn.commit()
                conn.close()
                viewEmbed = nextcord.Embed()
                viewEmbed.title = (f"{clothname} {emotes["emoteWardrobe"]}")
                if outfitrarity == 3:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                viewEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                viewEmbed.add_field(name="Outfit", value=f'{outfitname}')
                viewEmbed.add_field(name="Name", value=f"{clothname}")
                viewEmbed.add_field(name="Rarity", value=f"{outfitrarity} {emotes["emoteStar"]}")
                if outfitrarity == 3:
                    viewEmbed.add_field(name="Value", value=f"3500 {emotes["emoteBling"]}")
                elif outfitrarity == 4:
                    viewEmbed.add_field(name="Value", value=f"7500 {emotes["emoteBling"]}")
                else:
                    viewEmbed.add_field(name="Value", value=f"10000 {emotes["emoteBling"]}")
                viewEmbed.set_image(clothimage)
                await inter.response.send_message(embed = viewEmbed)
        else:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT clothes.clothid, clothes.clothname, outfits.outfitname, outfits.outfitrarity, outfits.outfitimage FROM outfits INNER JOIN clothes ON (outfits.outfitid = clothes.outfitid) WHERE outfitname = ? ORDER BY clothes.clothname", (name,))
            results = cur.fetchone()
            if (results is None):
                await inter.response.send_message(f'''You either gave me an **incorrect outfit name**, or it **doesn't exist**! {emotes["emoteNikkiCry"]}''')
            else:
                results = cur.fetchall()
                clothname = results[0][1]
                outfitname = results[0][2]
                outfitrarity = results[0][3]
                outfitimage = results[0][4]
                conn.commit()
                conn.close()
                viewEmbed = nextcord.Embed()
                viewEmbed.title = (f"{outfitname} {emotes["emoteWardrobe"]}")
                if outfitrarity == 3:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                viewEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                viewEmbed.description = f'**Name:** {outfitname} - **Rarity:** {outfitrarity} {emotes["emoteStar"]}'
                clothes = ""
                compteur = 0
                for i in results:
                    compteur += 1
                compteur2 = 0
                for i in results:
                    compteur2 += 1
                    if compteur2 < compteur:
                        clothes += f'{i[1]}, '
                    else:
                        clothes += i[1]
                viewEmbed.add_field(name="Clothes", value=f"{clothes}")
                viewEmbed.set_image(outfitimage)
                await inter.response.send_message(embed = viewEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cView(bot))