import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cMiraLevel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="miralevel",
        description="Let you know your Mira Level and remaining Mira EXP before levelling up!",
    )   
    async def miralevel(
        self,
        inter: nextcord.Interaction, 
        type: int = nextcord.SlashOption(
            name="embed",
            description="Displays the command as an embed or not!",
            choices={"Yes please! :)": 1, "No thanks :(": 0},
        ),
        user: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist",
            description="View the Mira Level of a specified stylist!"
        ),
        ):
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()

        user = user or inter.user # si un user est spécifié, on le prend, sinon c'est l'auteur de l'interaction

        cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ? AND guildid = ?', (str(user.id), inter.guild_id,))
        results = cur.fetchone()
        if results is None:
            cur.execute(f'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)', ((str(user.id), 1, 1, 1, 0, '2000-01-01', '2000-01-01', inter.guild_id,)))
            results = (1, 1, 1)
        conn.commit()
        conn.close()
            
        if(type == 1):
            miralevelEmbed = nextcord.Embed()
            miralevelEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            miralevelEmbed.title = (f"Stylist {user.name}'s Mira Level {emotes['emoteMiraLevel']}")
            miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
            miralevelEmbed.add_field(name="Mira Level", value=f'{str((results[2]))} {emotes["emoteMiraLevel"]}')
            miralevelEmbed.add_field(name="Total Mira EXP", value=f"{str(results[1])} EXP {emotes['emoteMiraExp']}")
            miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} EXP {emotes['emoteMiraExp']}")
            await inter.response.send_message(embed = miralevelEmbed)
        else:
            await inter.response.send_message(f"{user.name}'s **Mira Level {emotes["emoteMiraLevel"]} : {results[2]}** - Total : **{results[1]} EXP {emotes["emoteMiraExp"]}** - Level :up: in **{neededXp - results[0]} EXP {emotes['emoteMiraExp']}**! {emotes["emoteNikkiWink"]}")

def setup(bot: commands.Bot):
    bot.add_cog(cMiraLevel(bot))