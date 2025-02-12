import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes

class cWelcomeEvent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if member.guild.id == 1323383627492364319:
            channel = self.bot.get_channel(1323572410452017193)
            welcomeEmbed = nextcord.Embed()
            await channel.send(member.mention)
            welcomeEmbed.title = f'Welcome, stylist {member.display_name}! {emotes["emoteNikkiKiss"]}'
            welcomeEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            welcomeEmbed.set_thumbnail('https://stickershop.line-scdn.net/stickershop/v1/product/28246239/LINEStorePC/main.png?v=1')
            try:
                welcomeEmbed.set_image(member.avatar.url)
            except:
                pass
            welcomeEmbed.description = f'''Hi there, {member.name}! I am __**Momo**__, yours truly **travel companion** for the {member.guild.name} server! For *safety reasons*, you __**must verify yourself in #verify-yourself-♡**__, and you will be able to talk in __**10 minutes**__. In the meantime, I invite you to wander through our different **discussion channels**, there are so many nice **nikki's** out there~ ! {emotes["emoteNikkiWink"]}'''
            await channel.send(embed=welcomeEmbed)
            try:
                await member.send(f'''Hi there, {member.display_name}! I am __**Momo**__, yours truly **travel companion** for the Nikkiscord server! For *safety reasons*, you __**must verify yourself in #verify-yourself-♡**__, and you will be able to talk in __**10 minutes**__. In the meantime, I invite you to wander through our different **discussion channels**, there are so many nice **nikki's** out there~ ! {emotes["emoteNikkiWink"]}''')
            except nextcord.Forbidden:
                pass
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO users (userid, level, totalxp, xp, blings, lastdailypull, lastdailyblings, guildid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (member.id, 1, 1, 1, 0, '2000-01-01', '2000-01-01', member.guild.id))
            cur.execute(f'SELECT xp, totalxp, level FROM users WHERE userID = ? AND guildid = ?', (member.id, member.guild.id))
            results = cur.fetchone()
        else:
            pass
                
def setup(bot: commands.Bot):
    bot.add_cog(cWelcomeEvent(bot))