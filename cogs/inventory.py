import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cInventory(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="inventory",
        description="Check your inventory!",
    )   
    async def inventory(
        self,
        inter: nextcord.Interaction,
        type: int = nextcord.SlashOption(
             name="imaged",
             description="Displays your inventory clothes one by one!",
             choices={"Yes please! :)": 1, "No thanks :(": 0},
        ),
        user: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist",
            description="View the inventory of a specified stylist!"
        ),
        ):
        user = user or inter.user
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(clothid) FROM obtained WHERE userid = ?", (user.id,))
        results = cur.fetchone()
        if (results == None):
            await inter.response.send_message(f'''{user.name}'s inventory is **empty**! {emotes["emoteNikkiCry"]}''')
        else:
            nbItems = results[0]
            cur.execute("SELECT clothes.clothname, outfits.outfitname, clothes.clothimage, outfits.outfitrarity FROM clothes LEFT OUTER JOIN outfits ON (outfits.outfitid = clothes.outfitid) INNER JOIN obtained ON (clothes.clothid = obtained.clothid) WHERE userid = ? ORDER BY outfitname, clothname ASC", (user.id,))
            results = cur.fetchall()
            conn.commit()
            conn.close()
            if type == 0:
                if nbItems > 10:

                    async def next_callback(interaction): # clic sur next
                        nonlocal compteur
                        if compteur >= nbItems:
                            compteur = 0
                        inventoryEmbed.clear_fields()
                        for i in results[compteur:]:
                            compteur += 1
                            inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
                            if compteur % 10 == 0:
                                break  
                        
                        inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=inventoryEmbed, view=myView)

                    async def previous_callback(interaction): # clic sur previous
                        nonlocal compteur
                        if compteur == nbItems:
                            if nbItems%10 == 0: # cas où le nombre d'items est un multiple de 10
                                compteur = nbItems-20
                            else:
                                compteur = nbItems-(nbItems%10)-10
                        else:
                            compteur -= 20
                        if compteur < 0:
                            if nbItems%10 == 0: # cas où le nombre d'items est un multiple de 10
                                compteur = nbItems-10
                            else:
                                compteur = nbItems-(nbItems%10)
                        inventoryEmbed.clear_fields()
                        for i in results[compteur:]:
                            compteur += 1
                            inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
                            if compteur % 10 == 0:
                                break  
                        
                        inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=inventoryEmbed, view=myView)

                    nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                    nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                    previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                    previousButton.callback = previous_callback
                    myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                    myView.add_item(previousButton)
                    myView.add_item(nextButton)

                    inventoryEmbed = nextcord.Embed()
                    inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                    inventoryEmbed.title = (f"{user.name}'s inventory {emotes["emotePendants"]}")
                    compteur = 0
                    for i in results:
                        compteur += 1
                        inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
                        if compteur % 10 == 0:
                            break

                    # compteur = 10, ici
                    inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                    inventoryEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=202412221051001")
                    await inter.response.send_message(embed = inventoryEmbed, view=myView)

                else:
                    inventoryEmbed = nextcord.Embed()
                    inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                    inventoryEmbed.title = (f"{user.name}'s inventory {emotes["emotePendants"]}")
                    for i in results:
                        inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)

                    inventoryEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=202412221051001")
                    await inter.response.send_message(embed = inventoryEmbed)

            else:
                    async def next_callback(interaction): # clic sur next
                        nonlocal compteur
                        if compteur >= nbItems:
                            compteur = 0
                        inventoryEmbed.clear_fields()
                        if results[compteur][3] == 3:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                        elif results[compteur][3] == 4:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                        else:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                        inventoryEmbed.add_field(name=f'Outfit', value=f'{results[compteur][1]}')
                        inventoryEmbed.add_field(name=f'Name', value=f'{results[compteur][0]}')
                        inventoryEmbed.add_field(name=f'Rarity', value=f'{results[compteur][3]} {emotes["emoteStar"]}')
                        inventoryEmbed.set_image(results[compteur][2])
                        compteur += 1
                        
                        inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=inventoryEmbed, view=myView)

                    async def previous_callback(interaction): # clic sur previous
                        nonlocal compteur
                        compteur -= 2
                        if compteur < 0:
                            compteur = nbItems-1
                        inventoryEmbed.clear_fields()
                        if results[compteur][3] == 3:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                        elif results[compteur][3] == 4:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                        else:
                            inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                        inventoryEmbed.add_field(name=f'Outfit', value=f'{results[compteur][1]}')
                        inventoryEmbed.add_field(name=f'Name', value=f'{results[compteur][0]}')
                        inventoryEmbed.add_field(name=f'Rarity', value=f'{results[compteur][3]} {emotes["emoteStar"]}')
                        inventoryEmbed.set_image(results[compteur][2])
                        compteur += 1
                        
                        inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                        await inter.edit_original_message(embed=inventoryEmbed, view=myView)

                    nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                    nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                    previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                    previousButton.callback = previous_callback
                    myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                    myView.add_item(previousButton)
                    myView.add_item(nextButton)

                    compteur = 0
                    inventoryEmbed = nextcord.Embed()
                    if results[compteur][3] == 3:
                        inventoryEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                    elif results[compteur][3] == 4:
                        inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                    else:
                        inventoryEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                    inventoryEmbed.title = (f"{user.name}'s inventory {emotes["emotePendants"]}")
                    inventoryEmbed.add_field(name=f'Outfit', value=f'{results[compteur][1]}')
                    inventoryEmbed.add_field(name=f'Name', value=f'{results[compteur][0]}')
                    inventoryEmbed.add_field(name=f'Rarity', value=f'{results[compteur][3]} {emotes["emoteStar"]}')
                    inventoryEmbed.set_image(results[compteur][2])
                    compteur += 1
                    inventoryEmbed.set_footer(text=f'{compteur} out of {nbItems}')
                    inventoryEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=202412221051001")
                    await inter.response.send_message(embed = inventoryEmbed, view=myView)



        
def setup(bot: commands.Bot):
    bot.add_cog(cInventory(bot))