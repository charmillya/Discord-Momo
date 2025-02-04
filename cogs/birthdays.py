import nextcord
import sqlite3
from nextcord.ext import commands

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
        def GetMonth(month)->str:
            if int(month) == 1:
                return "January"
            elif int(month) == 2:
                return "February"
            elif int(month) == 3:
                return "March"
            elif int(month) == 4:
                return "April"
            elif int(month) == 5:
                return "May"
            elif int(month) == 6:
                return "June"
            elif int(month) == 7:
                return "July"
            elif int(month) == 8:
                return "August"
            elif int(month) == 9:
                return "September"
            elif int(month) == 10:
                return "October"
            elif int(month) == 11:
                return "November"
            else:
                return "December"
            
        def GetDay(day)->str:
            if day == '01' or day == '21' or day == '31':
                return "st"
            elif day == '02' or day == '22':
                return "nd"
            elif day == '03' or day == '23':
                return "rd"
            else:
                return "th"
            
        def RemoveZero(day)->str:
            if int(day[0]) == 0:
                return day[1]
            else:
                return day

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