import nextcord
import sqlite3
from datetime import datetime
from nextcord.ext import commands, tasks
from assets.momoemotes import emotes
from assets.months_days_utility import *

class cBdayEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_for_birthday.start()

    @tasks.loop(hours=24)
    async def check_for_birthday(self):
        await self.bot.wait_until_ready()
        now = datetime.today().strftime('%m-%d')
        
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT * from users where birthday like ?", (('%%%%%' + str(now)),))
        results = cur.fetchall()
        if(results):
            for result in results:
                user = self.bot.get_user(result[0])
                try:
                    await user.send(f"Hi {user.name}! I sneaked into your DMs to wish you a **happy birthday**! May your year be blessed *and all* ~ {emotes['emoteNikkiKiss']}")
                    if(result[7] == 1323383627492364319):
                        channel = self.bot.get_channel(1334659853410369556)
                        bdayEmbed = nextcord.Embed()
                        bdayEmbed.title = f'Happy birthday, {user.display_name}! :birthday:'
                        date = datetime.now().strftime('%Y-%m-%d')
                        print(date)
                        bdayEmbed.description = f"Today **{GetMonth(date[5:7])} {RemoveZero(date[8:10])}{GetDay(date[8:10])}**, we're celebrating **{user.name}**'s birthday! **HAPPY BIRTHDAY!!** {emotes['emoteNikkiKiss']}\nAs a **birthday present**, you get **100,000** {emotes['emoteBling']} !!"
                        bdayEmbed.colour = nextcord.Colour.from_rgb(255, 112, 243)
                        bdayEmbed.set_image(user.display_avatar.url)
                        await channel.send(embed=bdayEmbed)
                        cur.execute("UPDATE users SET blings = ? WHERE userid = ? AND guildid = ?", (result[4]+100000, result[0], result[7],))
                        conn.commit()
                except Exception as e:
                    print(e.args)
        
def setup(bot: commands.Bot):
    bot.add_cog(cBdayEvent(bot))