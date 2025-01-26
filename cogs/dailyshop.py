import nextcord
import sqlite3
from datetime import datetime
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes

class cDailyShop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="dailyshop",
        description="Display the daily clothes shop!",
    )   
    async def dailyshop(
        self,
        inter: nextcord.Interaction
    ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT lastdailyshop from parametres")
        results = cur.fetchone()
        currDate = datetime.today().strftime('%Y-%m-%d')
        if results[0] != currDate:
            cur.execute("DELETE FROM dailyshop")
            conn.commit()
            cur.execute("SELECT * FROM clothes ORDER BY RANDOM() LIMIT 3")
            results = cur.fetchall()
            for item in results:
                cur.execute("INSERT INTO dailyshop VALUES (?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4],))
                conn.commit()
                cur.execute("UPDATE parametres SET lastdailyshop = ?", (currDate,))
                conn.commit()

        dailyShopEmbed = nextcord.Embed()
        dailyShopEmbed.title = "Daily Shop! :shopping_cart:"
        dailyShopEmbed.description = "Look at today's three pieces of clothing you can buy!"
        nbItems = 3
        compteur = 0
        cur.execute("SELECT * FROM dailyshop inner join outfits on (dailyshop.outfitid = outfits.outfitid)")
        results = cur.fetchall()

        async def previous_callback(interaction): # clic sur previous
            nonlocal compteur
            myView.remove_item(resumeButton)
            compteur -= 1
            if compteur < 1:
                compteur = nbItems
            dailyShopEmbed.clear_fields()
            dailyShopEmbed.add_field(name="Outfit", value=results[compteur-1][6])
            dailyShopEmbed.add_field(name="Name", value=results[compteur-1][2])
            dailyShopEmbed.add_field(name="Rarity", value=f'{str(results[compteur-1][8])} {emotes["emoteStar"]}')
            if results[compteur-1][8] == 3:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                dailyShopEmbed.add_field(name="Price", value=f'2500 {emotes["emoteBling"]}')
            elif results[compteur-1][8] == 4:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                dailyShopEmbed.add_field(name="Price", value=f'5000 {emotes["emoteBling"]}')
            else:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                dailyShopEmbed.add_field(name="Price", value=f'7500 {emotes["emoteBling"]}')
            dailyShopEmbed.add_field(name="Owned quantity", value=check_obtained(inter.user.id, inter.guild_id, results[compteur-1][0]))
            dailyShopEmbed.set_image(results[compteur-1][3])

            dailyShopEmbed.set_footer(text=f'{compteur} out of {nbItems}')
            await inter.edit_original_message(embed=dailyShopEmbed, view=myView)

        async def buy_callback(interaction):
            nonlocal compteur
            previousButton.disabled = True
            nextButton.disabled = True
            buyButton.disabled = True
            resumeButton.disabled = False
            myView.add_item(resumeButton)

            cur.execute("SELECT blings FROM users where userid = ? and guildid = ?", (inter.user.id, inter.guild_id,))
            resultsBlings = cur.fetchone()

            errorEmbed = nextcord.Embed()
            errorEmbed.title = "Error! :x:"
            errorEmbed.description = f'''You don't have **enough Blings** {emotes["emoteBling"]}! Your current balance: {resultsBlings[0]} {emotes["emoteBling"]}'''
            errorEmbed.color = nextcord.Color.red()

            if results[compteur-1][8] == 3 and resultsBlings[0] - 2500 < 0:
                await inter.edit_original_message(embed=errorEmbed, view=myView)
            elif results[compteur-1][8] == 4 and resultsBlings[0] - 5000 < 0:
                await inter.edit_original_message(embed=errorEmbed, view=myView)
            elif results[compteur-1][8] == 5 and resultsBlings[0] - 7500 < 0:
                await inter.edit_original_message(embed=errorEmbed, view=myView)
            else:
                cur.execute("SELECT quantity FROM obtained where userid = ? and guildid = ? and clothid = ?", (inter.user.id, inter.guild_id, results[compteur-1][0],))
                resultsObtained = cur.fetchone()

                successEmbed = nextcord.Embed()
                successEmbed.title = "Success! :white_check_mark:"
                successEmbed.description = f'''Thank you for your **purchase**! {emotes["emoteNikkiWink"]}'''
                if resultsObtained:
                    successEmbed.add_field(name="New owned quantity", value=resultsObtained[0]+1)
                else:
                    successEmbed.add_field(name="New owned quantity", value=1)
                successEmbed.color = nextcord.Color.green()

                if results[compteur-1][8] == 3:
                    cur.execute("UPDATE users set blings = ? where userid = ? and guildid = ?", (resultsBlings[0]-2500, inter.user.id, inter.guild_id))
                    conn.commit()
                    successEmbed.add_field(name="New balance", value=f'{resultsBlings[0]-2500} {emotes["emoteBling"]}')
                elif results[compteur-1][8] == 4:
                    cur.execute("UPDATE users set blings = ? where userid = ? and guildid = ?", (resultsBlings[0]-5000, inter.user.id, inter.guild_id))
                    conn.commit()
                    successEmbed.add_field(name="New balance", value=f'{resultsBlings[0]-5000} {emotes["emoteBling"]}')
                else:
                    cur.execute("UPDATE users set blings = ? where userid = ? and guildid = ?", (resultsBlings[0]-7500, inter.user.id, inter.guild_id))
                    conn.commit()
                    successEmbed.add_field(name="New balance", value=f'{resultsBlings[0]-7500} {emotes["emoteBling"]}')

                if resultsObtained is None: # si item acheté = item pas possédé par user
                    cur.execute("INSERT INTO obtained VALUES (?, ?, ?, ?)", (inter.user.id, results[compteur-1][0], 1, inter.guild_id,))
                    conn.commit()
                else:
                    cur.execute("UPDATE obtained SET quantity = ? WHERE userid = ? and clothid = ? and guildid = ?", (resultsObtained[0]+1, inter.user.id, results[compteur-1][0], inter.guild_id,))
                    conn.commit()
                
                successEmbed.set_image(results[compteur-1][3])

                await inter.edit_original_message(embed=successEmbed, view=myView)

        async def next_callback(interaction):
            nonlocal compteur
            myView.remove_item(resumeButton)
            compteur += 1
            if compteur > nbItems:
                compteur = 1
            dailyShopEmbed.clear_fields()
            dailyShopEmbed.add_field(name="Outfit", value=results[compteur-1][6])
            dailyShopEmbed.add_field(name="Name", value=results[compteur-1][2])
            dailyShopEmbed.add_field(name="Rarity", value=f'{str(results[compteur-1][8])} {emotes["emoteStar"]}')
            if results[compteur-1][8] == 3:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                dailyShopEmbed.add_field(name="Price", value=f'2500 {emotes["emoteBling"]}')
            elif results[compteur-1][8] == 4:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                dailyShopEmbed.add_field(name="Price", value=f'5000 {emotes["emoteBling"]}')
            else:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                dailyShopEmbed.add_field(name="Price", value=f'7500 {emotes["emoteBling"]}')
            dailyShopEmbed.add_field(name="Owned quantity", value=check_obtained(inter.user.id, inter.guild_id, results[compteur-1][0]))
            dailyShopEmbed.set_image(results[compteur-1][3])

            dailyShopEmbed.set_footer(text=f'{compteur} out of {nbItems}')
            await inter.edit_original_message(embed=dailyShopEmbed, view=myView)

        async def resume_shopping_callback(interaction):
            nextButton.disabled = False
            previousButton.disabled = False
            buyButton.disabled = False
            myView.remove_item(resumeButton)
            dailyShopEmbed.clear_fields()
            dailyShopEmbed.add_field(name="Outfit", value=results[compteur-1][6])
            dailyShopEmbed.add_field(name="Name", value=results[compteur-1][2])
            dailyShopEmbed.add_field(name="Rarity", value=f'{str(results[compteur-1][8])} {emotes["emoteStar"]}')
            if results[compteur-1][8] == 3:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
                dailyShopEmbed.add_field(name="Price", value=f'2500 {emotes["emoteBling"]}')
            elif results[compteur-1][8] == 4:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
                dailyShopEmbed.add_field(name="Price", value=f'5000 {emotes["emoteBling"]}')
            else:
                dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
                dailyShopEmbed.add_field(name="Price", value=f'7500 {emotes["emoteBling"]}')
            dailyShopEmbed.add_field(name="Owned quantity", value=check_obtained(inter.user.id, inter.guild_id, results[compteur-1][0]))
            dailyShopEmbed.set_image(results[compteur-1][3])

            dailyShopEmbed.set_footer(text=f'{compteur} out of {nbItems}')
            await inter.edit_original_message(embed=dailyShopEmbed, view=myView)

        def check_obtained(userid, guildid, clothid)->str:
            cur.execute("SELECT quantity FROM obtained where userid = ? and guildid = ? and clothid = ?", (userid, guildid, clothid,))
            resultsObtained = cur.fetchone()
            if resultsObtained:
                return resultsObtained[0]
            else:
                return "0"

            
        compteur = 1

        dailyShopEmbed.add_field(name="Outfit", value=results[compteur-1][6])
        dailyShopEmbed.add_field(name="Name", value=results[compteur-1][2])
        dailyShopEmbed.add_field(name="Rarity", value=f'{str(results[compteur-1][8])} {emotes["emoteStar"]}')
        if results[compteur-1][8] == 3:
            dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(145, 105, 255)
            dailyShopEmbed.add_field(name="Price", value=f'2500 {emotes["emoteBling"]}')
        elif results[compteur-1][8] == 4:
            dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 250)
            dailyShopEmbed.add_field(name="Price", value=f'5000 {emotes["emoteBling"]}')
        else:
            dailyShopEmbed.colour = nextcord.colour.Color.from_rgb(255, 94, 164)
            dailyShopEmbed.add_field(name="Price", value=f'7500 {emotes["emoteBling"]}')
        dailyShopEmbed.add_field(name="Owned quantity", value=check_obtained(inter.user.id, inter.guild_id, results[compteur-1][0]))
        dailyShopEmbed.set_image(results[compteur-1][3])
        dailyShopEmbed.set_footer(text=f'{compteur} out of {nbItems}')
        nextButton = Button(label="Next!", style=ButtonStyle.blurple)
        nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
        previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
        previousButton.callback = previous_callback
        buyButton = Button(label="Buy!", style=ButtonStyle.blurple)
        buyButton.callback = buy_callback
        resumeButton = Button(label="Go back to shopping!", style=ButtonStyle.blurple)
        resumeButton.callback = resume_shopping_callback # affectation de la fonction event "on_click" au bouton
        myView = View(timeout=200) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
        myView.add_item(previousButton)
        myView.add_item(buyButton)
        myView.add_item(nextButton)
        await inter.response.send_message(embed = dailyShopEmbed, view=myView)


def setup(bot: commands.Bot):
    bot.add_cog(cDailyShop(bot))