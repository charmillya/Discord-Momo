import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
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
                clothid = results[0]
                clothname = results[1]
                clothimage = results[2]
                outfitname = results[3]
                outfitrarity = results[4]
                cur.execute("SELECT quantity FROM obtained WHERE clothid = ? AND userid = ? AND guildid = ?", (clothid, inter.user.id, inter.guild_id,))
                results = cur.fetchone()
                if results is None:
                    quantity = 0   
                else:
                    quantity = results[0]
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
                    viewEmbed.add_field(name="Value", value=f"1500 {emotes["emoteBling"]}")
                elif outfitrarity == 4:
                    viewEmbed.add_field(name="Value", value=f"3500 {emotes["emoteBling"]}")
                else:
                    viewEmbed.add_field(name="Value", value=f"5000 {emotes["emoteBling"]}")
                if quantity > 0:
                    viewEmbed.add_field(name="Owned", value=f"Quantity: **{quantity}**")
                else:
                    viewEmbed.add_field(name="Owned", value=":x:")
                viewEmbed.set_image(clothimage)
                await inter.response.send_message(embed = viewEmbed)
        else: # outfit view
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT clothes.clothid, clothes.clothname, outfits.outfitname, outfits.outfitrarity, outfits.outfitimage, outfits.outfitid, clothes.clothimage FROM outfits INNER JOIN clothes ON (outfits.outfitid = clothes.outfitid) WHERE outfitname = ? ORDER BY clothes.clothname", (name,))
            results = cur.fetchone()
            if (results is None):
                await inter.response.send_message(f'''You either gave me an **incorrect outfit name**, or it **doesn't exist**! {emotes["emoteNikkiCry"]}''')
            else:
                results = cur.fetchall()
                clothname = results[0][1]
                outfitname = results[0][2]
                outfitrarity = results[0][3]
                outfitimage = results[0][4]
                outfitid = results[0][5]
                cur.execute("SELECT COUNT(clothid) FROM clothes WHERE outfitid = ?", (outfitid,))
                resultsCount = cur.fetchone()
                nbItems = resultsCount[0]
                conn.commit()
                conn.close()


                async def next_callback(interaction): # clic sur next
                    nonlocal compteur
                    if compteur >= nbItems:
                        compteur = 0
                    if compteur != 0:
                        viewEmbed.clear_fields()
                        if results[compteur-1][3] == 3:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                        elif results[compteur-1][3] == 4:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                        else:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                        viewEmbed.add_field(name=f'Name', value=f'{results[compteur-1][1]}')
                        viewEmbed.set_image(results[compteur-1][6])
                        compteur += 1
                            
                        viewEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=viewEmbed)
                    else:
                        viewEmbed.clear_fields()
                        viewEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                        viewEmbed.description = f'**Rarity:** {outfitrarity} {emotes["emoteStar"]}'
                        clothes = ""
                        compteurClothes = 0
                        for i in results:
                            compteurClothes += 1
                        compteur2 = 0
                        for i in results:
                            compteur2 += 1
                            if compteur2 < compteurClothes:
                                clothes += f'{i[1]}, '
                            else:
                                clothes += i[1]
                        compteur = 0
                        viewEmbed.add_field(name="Clothes", value=f"{clothes}")
                        viewEmbed.set_footer(text=f'{compteur+1} out of {nbItems}')
                        viewEmbed.set_image(outfitimage)
                        nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                        nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                        previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                        previousButton.callback = previous_callback
                        myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                        myView.add_item(previousButton)
                        myView.add_item(nextButton)
                        compteur = 1
                        await inter.edit_original_message(embed = viewEmbed)

                async def previous_callback(interaction): # clic sur previous
                    nonlocal compteur
                    compteur -= 2
                    if compteur != 0:
                        if compteur < 0:
                            compteur = nbItems-1
                        viewEmbed.clear_fields()
                        if results[compteur-1][3] == 3:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                        elif results[compteur-1][3] == 4:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                        else:
                            viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                        viewEmbed.add_field(name=f'Name', value=f'{results[compteur-1][1]}')
                        viewEmbed.set_image(results[compteur-1][6])
                        compteur += 1
                            
                        viewEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=viewEmbed)
                    else:
                        viewEmbed.clear_fields()
                        viewEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                        viewEmbed.description = f'**Rarity:** {outfitrarity} {emotes["emoteStar"]}'
                        clothes = ""
                        compteurClothes = 0
                        for i in results:
                            compteurClothes += 1
                        compteur2 = 0
                        for i in results:
                            compteur2 += 1
                            if compteur2 < compteurClothes:
                                clothes += f'{i[1]}, '
                            else:
                                clothes += i[1]
                        compteur = 0
                        viewEmbed.add_field(name="Clothes", value=f"{clothes}")
                        viewEmbed.set_footer(text=f'{compteur+1} out of {nbItems}')
                        viewEmbed.set_image(outfitimage)
                        nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                        nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                        previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                        previousButton.callback = previous_callback
                        myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                        myView.add_item(previousButton)
                        myView.add_item(nextButton)
                        compteur = 1
                        await inter.edit_original_message(embed = viewEmbed, view=myView)


                viewEmbed = nextcord.Embed()
                viewEmbed.title = (f"{outfitname} {emotes["emoteWardrobe"]}")
                if outfitrarity == 3:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                elif outfitrarity == 4:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                else:
                    viewEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                viewEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
                viewEmbed.description = f'**Rarity:** {outfitrarity} {emotes["emoteStar"]}'
                clothes = ""
                compteurClothes = 0
                for i in results:
                    compteurClothes += 1
                compteur2 = 0
                for i in results:
                    compteur2 += 1
                    if compteur2 < compteurClothes:
                        clothes += f'{i[1]}, '
                    else:
                        clothes += i[1]
                compteur = 0
                viewEmbed.add_field(name="Clothes", value=f"{clothes}")
                viewEmbed.set_footer(text=f'{compteur+1} out of {nbItems}')
                viewEmbed.set_image(outfitimage)
                nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                previousButton.callback = previous_callback
                myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                myView.add_item(previousButton)
                myView.add_item(nextButton)
                compteur = 1
                await inter.response.send_message(embed = viewEmbed, view=myView)

        
def setup(bot: commands.Bot):
    bot.add_cog(cView(bot))