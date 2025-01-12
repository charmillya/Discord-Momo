import nextcord
import sqlite3
from nextcord.ext import commands
from assets.momoemotes import emotes
from assets.neededxp import neededXp

class cInventory(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="inventory",
        description="Checks your inventory!",
    )   
    async def inventory(
        self,
        inter: nextcord.Interaction,
        # type: int = nextcord.SlashOption(
        #     name="imaged",
        #     description="Displays your inventory clothes one by one!",
        #     choices={"Yes please! :)": 1, "No thanks :(": 0},
        # ),
        user: nextcord.Member = nextcord.SlashOption(
            required=False,
            name="stylist",
            description="View the inventory of a specified stylist!"
        ),
        ):
        user = user or inter.user
        conn = sqlite3.connect('momodb.db')
        cur = conn.cursor()
        cur.execute("SELECT clothes.clothname, outfits.outfitname, clothes.clothimage FROM clothes LEFT OUTER JOIN outfits ON (outfits.outfitid = clothes.outfitid) INNER JOIN obtained ON (clothes.clothid = obtained.clothid) WHERE userid = ? ORDER BY outfitname, clothname ASC", (user.id,))
        results = cur.fetchall()
        conn.commit()
        conn.close()
        inventoryEmbed = nextcord.Embed()
        inventoryEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
        inventoryEmbed.title = (f"{user.name}'s inventory {emotes["emotePendants"]}")
        inventoryEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=20241222105801")
        # if type == 0:
        if (results != []):
            for i in results:
                inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
        else:
            inventoryEmbed.description = "Your inventory is empty!"
        await inter.response.send_message(embed = inventoryEmbed)
        # else:
        #     if (results != []):
        #         for i in results:
        #             inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
        #             inventoryEmbed.set_image(i[2])
        #     else:
        #         inventoryEmbed.description = "Your inventory is empty!"
        #     await inter.response.send_message(embed = inventoryEmbed)

        
def setup(bot: commands.Bot):
    bot.add_cog(cInventory(bot))