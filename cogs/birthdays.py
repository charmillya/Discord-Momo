import nextcord
import sqlite3
from nextcord.ext import commands
from assets.months_days_utility import *

class cBirthdays(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="birthdays",
        description="List the 10 upcoming birthdays in the server!",
    )   
        
    async def view(
        self,
        inter: nextcord.Interaction,
        ):

        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT userid, birthday FROM users WHERE guildid = ? ORDER BY (CAST(strftime('%m%d', birthday) AS INTEGER) >= CAST(strftime('%m%d', DATE('now')) AS INTEGER)) DESC, CAST(strftime('%m%d', birthday) AS INTEGER) ASC LIMIT 10", (inter.guild_id,))
        results = cur.fetchall()
    
        birthdaysEmbed = nextcord.Embed()
        birthdaysEmbed.title = "Upcoming birthdays! :cake:"
        birthdaysEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        birthdaysEmbed.description = f"Here are the 10 upcoming birthdays for this server:"
        for birthday in results:
            if birthday[1] != None:
                member = self.bot.get_user(birthday[0])
                birthdaysEmbed.add_field(name=member.display_name, value=f"{GetMonth(birthday[1][5:7])} {RemoveZero(birthday[1][8:10])}{GetDay(birthday[1][8:10])}")
        birthdaysEmbed.set_footer(text="Use /setbirthday to register yours!")
        await inter.response.send_message(embed=birthdaysEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cBirthdays(bot))