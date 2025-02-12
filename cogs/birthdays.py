import nextcord
import sqlite3
from nextcord import File, ButtonStyle, Embed, Color
from nextcord.ext import commands
from nextcord.ui import Button, View
from assets.momoemotes import emotes
from assets.months_days_utility import *

class cBirthdays(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="birthdays",
        description="List all the registered birthdays in the server!",
    )   
        
    async def birthdays(
        self,
        inter: nextcord.Interaction,
        ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(userid) FROM users WHERE birthday IS NOT NULL AND guildid = ?", (inter.guild_id,))
        results = cur.fetchone()
        if (results[0] == 0):
            await inter.response.send_message(f'''The birthdays list for this server is **empty**! {emotes["emoteNikkiCry"]}''')
        else:
            nbBirthdays = results[0]
            cur.execute("SELECT userid, birthday FROM users WHERE birthday IS NOT NULL AND guildid = ? ORDER BY birthday", (inter.guild_id,))
            results = cur.fetchall()
            conn.commit()
            conn.close()
            if nbBirthdays > 10:
                async def next_callback(interaction): # clic sur next
                    nonlocal compteur
                    if compteur >= nbBirthdays:
                        compteur = 0
                    birthdaysEmbed.clear_fields()
                    for i in results[compteur:]:
                        try:
                            selectedUser = self.bot.get_user(i[0])
                            birthdaysEmbed.add_field(name=f'{selectedUser.display_name}', value=f'{GetMonth(i[1][5:7])} {RemoveZero(i[1][8:10])}{GetDay(i[1][8:10])} {i[1][0:4]}', inline=False)
                            compteur += 1
                            if compteur % 10 == 0:
                                break  
                        except:
                            pass
                    
                    birthdaysEmbed.set_footer(text=f'{compteur} out of {nbBirthdays}')
                    await inter.edit_original_message(embed=birthdaysEmbed, view=myView)

                async def previous_callback(interaction): # clic sur previous
                    nonlocal compteur
                    if compteur == nbBirthdays:
                        if nbBirthdays%10 == 0: # cas où le nombre d'items est un multiple de 10
                            compteur = nbBirthdays-20
                        else:
                            compteur = nbBirthdays-(nbBirthdays%10)-10
                    else:
                        compteur -= 20
                    if compteur < 0:
                        if nbBirthdays%10 == 0: # cas où le nombre d'items est un multiple de 10
                            compteur = nbBirthdays-10
                        else:
                            compteur = nbBirthdays-(nbBirthdays%10)
                    birthdaysEmbed.clear_fields()
                    for i in results[compteur:]:
                        try:
                            selectedUser = self.bot.get_user(i[0])
                            birthdaysEmbed.add_field(name=f'{selectedUser.display_name}', value=f'{GetMonth(i[1][5:7])} {RemoveZero(i[1][8:10])}{GetDay(i[1][8:10])} {i[1][0:4]}', inline=False)
                            compteur += 1
                            if compteur % 10 == 0:
                                break
                        except:
                            pass
                     
                    birthdaysEmbed.set_footer(text=f'{compteur} out of {nbBirthdays}')
                    await inter.edit_original_message(embed=birthdaysEmbed, view=myView)

                if(nbBirthdays > 1):
                    nextButton = Button(label="Next!", style=ButtonStyle.blurple)
                    nextButton.callback = next_callback # affectation de la fonction event "on_click" au bouton
                    previousButton = Button(label="Previous!", style=ButtonStyle.blurple)
                    previousButton.callback = previous_callback
                    myView = View(timeout=180) # myview est un objet View, en gros c'est l'ui, les trucs interactifs qu'on va afficher
                    myView.add_item(previousButton)
                    myView.add_item(nextButton)

                birthdaysEmbed = nextcord.Embed()
                birthdaysEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                birthdaysEmbed.title = (f"{inter.guild.name}'s birthdays :cake:")
                compteur = 0
                for i in results:
                    try:
                        selectedUser = self.bot.get_user(i[0])
                        birthdaysEmbed.add_field(name=f'{selectedUser.display_name}', value=f'{GetMonth(i[1][5:7])} {RemoveZero(i[1][8:10])}{GetDay(i[1][8:10])} {i[1][0:4]}', inline=False)
                        compteur += 1
                        if compteur % 10 == 0:
                            break
                    except:
                        pass

                # compteur = 10, ici
                birthdaysEmbed.set_footer(text=f'{compteur} out of {nbBirthdays}')
                birthdaysEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=202412221051001")
                if(nbBirthdays > 1):
                    await inter.response.send_message(embed = birthdaysEmbed, view=myView)
                else:
                    await inter.response.send_message(embed = birthdaysEmbed)
                    
            else:
                birthdaysEmbed = nextcord.Embed()
                birthdaysEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
                birthdaysEmbed.title = (f"{inter.guild.name}'s birthdays :cake:")
                for i in results:
                    try:
                        selectedUser = self.bot.get_user(i[0])
                        birthdaysEmbed.add_field(name=f'{selectedUser.display_name}', value=f'{GetMonth(i[1][5:7])} {RemoveZero(i[1][8:10])}{GetDay(i[1][8:10])} {i[1][0:4]}', inline=False)
                    except:
                        pass
                birthdaysEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=202412221051001")
                await inter.response.send_message(embed = birthdaysEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cBirthdays(bot))