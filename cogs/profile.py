import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes

class cProfile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="profile",
        description="Display your MomoBot profile!",
    )   
    async def profile(
        self,
        inter: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist",
            description="View the MomoBot profile of a specified stylist!"
        ),
        ):
        user = user or inter.user
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT level, blings, lastdailyblings, lastdailypull, birthday, totalxp from users where userid = ? and guildid = ?", (user.id, inter.guild.id,))
        results = cur.fetchone()

        level = results[0]
        blings = results[1]
        if results[2] == '2000-01-01':
            lastdailyblings = "Never claimed yet!"
        else:
            lastdailyblings = results[2]

        if results[3] == '2000-01-01':
            lastdailypull = "Never claimed yet!"
        else:
            lastdailypull = results[3]

        if results[4] is None:
            birthday = "Not set: use /setbirthday to set it!"
        else:
            birthday = results[4]
            
        xp = results[5]

        cur.execute("SELECT COUNT(clothid) FROM obtained WHERE userid = ? AND guildid = ?", (user.id, inter.guild.id,))
        results = cur.fetchone()

        totalclothes = results[0]

        profileEmbed = nextcord.Embed()
        profileEmbed.title = f"{user.display_name}'s profile!"
        profileEmbed.add_field(name=f"Username", value=user.name, inline=True)
        profileEmbed.add_field(name=f"User ID", value=user.id, inline=True)
        profileEmbed.add_field(name=f"Account created on", value=user.created_at.strftime('%d-%m-%Y'), inline=True)
        profileEmbed.add_field(name=f"Total messages sent", value=xp, inline=True)
        profileEmbed.add_field(name=f"Quantity of clothes owned", value=totalclothes, inline=True)
        profileEmbed.add_field(name=f"Mira Level {emotes["emoteMiraLevel"]}", value=level, inline=True)
        profileEmbed.add_field(name=f"Blings {emotes["emoteBling"]}", value=blings, inline=True)
        profileEmbed.add_field(name=f"Last daily: Blings {emotes["emoteBling"]}", value=lastdailyblings, inline=True)
        profileEmbed.add_field(name=f"Last daily: Resonance", value=lastdailypull, inline=True)
        profileEmbed.add_field(name=f"Birthday :cake:", value=birthday, inline=True)

        profileEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
        profileEmbed.set_thumbnail(user.avatar.url)
        await inter.response.send_message(embed=profileEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cProfile(bot))