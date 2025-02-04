import nextcord
import sqlite3
from nextcord.ext import commands

class cSetBirthday(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="setbirthday",
        description="Set your birthday to get a special gift on this day!",
    )   
    async def setbirthday(
        self,
        inter: nextcord.Interaction,
        year: str = nextcord.SlashOption(
            required=True,
            name="year",
            description="Your birthday year (i.e. : 2007)!"
        ),
        month: str = nextcord.SlashOption(
            required=True,
            name="month",
            description="Your birthday month (i.e. : 02)!"
        ),
        day: str = nextcord.SlashOption(
            required=True,
            name="day",
            description="Your birthday day (i.e. : 24)!"
        ),
        ):
        birthday = year+"-"+month+"-"+day
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT * from users where userid = ? and guildid = ?", (inter.user.id, inter.guild.id,))
        results = cur.fetchone()
        if results[8] != None:
            await inter.response.send_message(f"{inter.user.mention}, you have **already set** your birthday! :birthday:")
        elif len(year) != 4 or len(month) != 2 or len(day) != 2 or len(birthday) != 10:
            await inter.response.send_message(f"{inter.user.mention}, the **format** of the birthday you provided is **incorrect**! Please follow the **provided examples**.")
        else:
            cur.execute("UPDATE users SET birthday = ? WHERE userid = ? and guildid = ?", (birthday, inter.user.id, inter.guild.id,))
            conn.commit()
            setBdayEmbed = nextcord.Embed()
            setBdayEmbed.title = "Birthday set! :cake:"
            setBdayEmbed.colour = nextcord.colour.Color.from_rgb(255, 112, 243)
            setBdayEmbed.description = f"{inter.user.mention}, your **birthday** has been set to the following date: **{birthday}**!"
            setBdayEmbed.set_footer(text="If you want to change your birthday, please contact my developer @charmillya!")
            setBdayEmbed.set_thumbnail(inter.user.avatar.url)
            await inter.response.send_message(embed=setBdayEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cSetBirthday(bot))