import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes

class cLeaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="leaderboard",
        description="Check the 10 top stylists of our server!",
    )   
    async def blings(
        self,
        inter: nextcord.Interaction,
        type: int = nextcord.SlashOption(
            name="type",
            choices={"Mira EXP": 1, "Blings": 2, "Both": 3},
        ),
        ):
        if type == 1:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT userid, level, totalxp FROM users WHERE guildid = ? ORDER BY totalxp DESC LIMIT 10", (inter.guild_id,))
            results = cur.fetchall()
            conn.commit()
            conn.close()
            leaderboardEmbed = nextcord.Embed()
            leaderboardEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            leaderboardEmbed.title = (f"Top 10 Stylists : Mira EXP {emotes["emoteMiraExp"]}")
            leaderboardEmbed.description = f'Here are our top stylists based on Mira EXP {emotes["emoteMiraExp"]} ! {emotes["emoteNikkiWink"]}'
            leaderboardEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/a/aa/Mira_EXP_Icon.png/revision/latest?cb=20241221113200")
            counter = 0
            for i in results:
                counter += 1
                currUser = await self.bot.fetch_user(i[0])
                if counter == 1:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :first_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}')
                elif counter == 2:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :second_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}')
                elif counter == 3:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :third_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}')
                else:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name}', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}')
            await inter.response.send_message(embed=leaderboardEmbed)
        elif type == 2:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT userid, blings FROM users WHERE guildid = ? ORDER BY blings DESC LIMIT 10", (inter.guild_id,))
            results = cur.fetchall()
            conn.commit()
            conn.close()
            leaderboardEmbed = nextcord.Embed()
            leaderboardEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            leaderboardEmbed.title = (f"Top 10 Stylists : Blings {emotes["emoteBling"]}")
            leaderboardEmbed.description = f'Here are our top stylists based on Blings {emotes["emoteBling"]} ! {emotes["emoteNikkiWink"]}'
            leaderboardEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/d/dd/Bling_Icon.png/revision/latest?cb=20241208230112")
            counter = 0
            for i in results:
                counter += 1
                currUser = await self.bot.fetch_user(i[0])
                if counter == 1:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :first_place:', value=f'**Blings:** {i[1]} {emotes["emoteBling"]}')
                elif counter == 2:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :second_place:', value=f'**Blings:** {i[1]} {emotes["emoteBling"]}')
                elif counter == 3:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :third_place:', value=f'**Blings:** {i[1]} {emotes["emoteBling"]}')
                else:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name}', value=f'**Blings:** {i[1]} {emotes["emoteBling"]}')
            await inter.response.send_message(embed=leaderboardEmbed)
        else:
            conn = sqlite3.connect('momodb.db')
            cur = conn.cursor()
            cur.execute("SELECT userid, level, totalxp, blings FROM users WHERE guildid = ? ORDER BY totalxp * 100 + blings DESC LIMIT 10", (inter.guild_id,))
            results = cur.fetchall()
            conn.commit()
            conn.close()
            leaderboardEmbed = nextcord.Embed()
            leaderboardEmbed.colour = nextcord.colour.Color.from_rgb(255, 187, 69)
            leaderboardEmbed.title = (f"Top 10 Stylists : Mira EXP {emotes["emoteMiraExp"]} + Blings {emotes["emoteBling"]}")
            leaderboardEmbed.description = f'Here are our top stylists based on Mira EXP {emotes["emoteMiraExp"]} and Blings {emotes["emoteBling"]} ! {emotes["emoteNikkiWink"]}'
            leaderboardEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/d/dd/Bling_Icon.png/revision/latest?cb=20241208230112")
            counter = 0
            for i in results:
                counter += 1
                currUser = await self.bot.fetch_user(i[0])
                if counter == 1:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :first_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}\n**Blings:** {i[3]} {emotes["emoteBling"]}')
                elif counter == 2:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :second_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}\n**Blings:** {i[3]} {emotes["emoteBling"]}')
                elif counter == 3:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name} :third_place:', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}\n**Blings:** {i[3]} {emotes["emoteBling"]}')
                else:
                    leaderboardEmbed.add_field(name=f'Top {counter} - {currUser.name}', value=f'**Level:** {i[1]} {emotes["emoteMiraLevel"]}\n**Total Mira EXP:** {i[2]} {emotes["emoteMiraExp"]}\n**Blings:** {i[3]} {emotes["emoteBling"]}')
            await inter.response.send_message(embed=leaderboardEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cLeaderboard(bot))