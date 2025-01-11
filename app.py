import nextcord
import sqlite3
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.message_content = True

#   for i in levelsFileData['user']: # test sortie de tous les utilisateurs dans levels.json avec leur xp
#       print(f"User {i['name']} - Level {i['level']} - {i['xp']} xp")

bot = commands.Bot(command_prefix = "momo ", intents=intents) # instanciation de l'objet bot

nikkisID = '1323383627492364319' # identifiant du serveur nikki's
emotes = {"emoteNikkiWink": "<:nikki_wink:1326685739148116009>",
           "emoteNikkiKiss": "<:nikki_kiss:1326589108361101405>", 
           "emoteMiraLevel": "<:mira_level:1327334099874087043>", 
           "emoteMiraExp": "<:mira_exp:1327333514831728720>", 
           "emotePendants": "<:pendants:1327454772592246794>", 
           "emoteWardrobe": "<:wardrobe:1327454758977536123>"}

# levelling system

neededXp = 50 # needed xp before levelling up

@bot.event # level system
async def on_message(message):
    user = message.author.id
    conn = sqlite3.connect('momodb.db')
    cur = conn.cursor()
    cur.execute(f'SELECT xp, totalxp, level FROM users WHERE userID = ?', (user,))
    results = cur.fetchone()

    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (user, 1, 1, 1))
        cur.execute(f'SELECT xp, totalxp, level FROM users WHERE userID = ?', (user,))
        results = cur.fetchone()

    old_xp = results[0] ##the first item in the index, in this case, xp
    old_level = results[2] ## the second item in the index, in this case, level
    perm_xp = results[1]+1
    new_xp = old_xp + 1
    if new_xp == neededXp: #this is where you set the threshold for leveling up to the first level
        new_level = old_level+1
        new_xp = 0
        await message.channel.send(f":up: Congrats {message.author.mention}, you gained a **Mira Level** {emotes['emoteMiraLevel']} and you are now Level **{new_level}**!")
    else:
        new_level = old_level
    ###add more logic here for successive level-ups
    cur.execute('UPDATE users SET xp = ?, totalXp = ?, level = ? WHERE userid = ?', (new_xp, perm_xp, new_level, user,))
    conn.commit()
    conn.close()
    await bot.process_commands(message)

@bot.slash_command( # check level and xp remaining
    name="miralevel",
    description="Lets you know your Mira Level and remaining Mira EXP before levelling up!",
)   
async def miralevel(
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

    cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ?', (str(user.id),))
    results = cur.fetchone()
    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', ((str(user.id), 1, 1, 1)))
        results = (1, 1, 1)
    conn.commit()
    conn.close()
        
    if(type == 1):
        miralevelEmbed = nextcord.Embed()
        miralevelEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
        miralevelEmbed.title = (f"Stylist {user.name}'s Mira Level {emotes['emoteMiraLevel']}")
        miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
        miralevelEmbed.add_field(name="Mira Level", value=f'{str((results[2]))} {emotes["emoteMiraLevel"]}')
        miralevelEmbed.add_field(name="Total", value=f"{str(results[1])} EXP {emotes['emoteMiraExp']}")
        miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} EXP {emotes['emoteMiraExp']}")
        await inter.response.send_message(embed = miralevelEmbed)
    else:
        await inter.response.send_message(f"{user.name}'s **Mira Level {emotes["emoteMiraLevel"]} : {results[2]}** - Total : **{results[1]} EXP {emotes["emoteMiraExp"]}** - Level :up: in **{neededXp - results[0]} EXP {emotes['emoteMiraExp']}**! {emotes["emoteNikkiWink"]}")

# outfit management

@bot.slash_command(
    name="daily",
    description="Claims your daily random piece of clothing!",
)   
async def daily(
    inter: nextcord.Interaction
    ):
    conn = sqlite3.connect('momodb.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(clothname) FROM clothes")
    results = cur.fetchone()
    nbClothes = results[0]
    cur.execute("SELECT COUNT(userid) FROM obtained WHERE userid = ?", (inter.user.id,))
    results = cur.fetchone()
    if nbClothes > results[0]:
        cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, obtained.userid, obtained.clothid FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) LEFT OUTER JOIN obtained ON (obtained.clothid = clothes.clothid) ORDER BY RANDOM()")
        results = cur.fetchone()
        selectedClothID = results[1]
        obtainedUserID = results[4]
        obtainedClothID = results[5]
        while (obtainedUserID == inter.user.id and obtainedClothID == selectedClothID):
            cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, obtained.userid, obtained.clothid FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) LEFT OUTER JOIN obtained ON (obtained.clothid = clothes.clothid) ORDER BY RANDOM()")
            results = cur.fetchone()
            selectedClothID = results[1]
            obtainedUserID = results[4]
            obtainedClothID = results[5]
        cur.execute("INSERT INTO obtained VALUES (?, ?)", (inter.user.id, selectedClothID,))
        conn.commit()
        conn.close()
        dailyEmbed = nextcord.Embed()
        dailyEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
        dailyEmbed.title = (f"Your daily piece of clothing {emotes["emoteWardrobe"]}")
        dailyEmbed.description = "The following piece of clothing has been added to your inventory!"
        dailyEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
        dailyEmbed.add_field(name="Outfit", value=f'{str((results[0]))}')
        dailyEmbed.add_field(name="Name", value=f"{str(results[2])}")
        dailyEmbed.set_image(results[3])
        await inter.response.send_message(embed = dailyEmbed)
    else:
        await inter.response.send_message("You've already collected all pieces of clothing!")

@bot.slash_command(
    name="inventory",
    description="Checks your inventory!",
)   
async def inventory(
    inter: nextcord.Interaction,
    user: nextcord.Member = nextcord.SlashOption(
        required=False,
        name="stylist",
        description="View the inventory of a specified stylist!"
    ),
    ):
    user = user or inter.user
    conn = sqlite3.connect('momodb.db')
    cur = conn.cursor()
    cur.execute("SELECT clothes.clothname, outfits.outfitname FROM clothes LEFT OUTER JOIN outfits ON (outfits.outfitid = clothes.outfitid) INNER JOIN obtained ON (clothes.clothid = obtained.clothid) WHERE userid = ? ORDER BY outfitname, clothname ASC", (inter.user.id,))
    results = cur.fetchall()
    conn.commit()
    conn.close()
    inventoryEmbed = nextcord.Embed()
    inventoryEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
    inventoryEmbed.title = (f"{user.name}'s inventory {emotes["emotePendants"]}")
    inventoryEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/b/b7/Icon_Pendants.png/revision/latest?cb=20241222105801")
    for i in results:
        inventoryEmbed.add_field(name=f'{str((i[1]))}', value=f'{str((i[0]))}', inline=False)
    await inter.response.send_message(embed = inventoryEmbed)
    
# commands

@bot.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! Momo v0.1 {emotes["emoteNikkiKiss"]}')

@bot.slash_command( # online command
    name="online",
    description="Tests if I'm online!",
)   
async def online(inter: nextcord.Interaction) -> None:
    await inter.response.send_message(f'I am alive! {emotes["emoteNikkiKiss"]}')

@bot.slash_command( # echo command
    name="echo",
    description="I repeat what you say!",
)  
async def echo(interaction: nextcord.Interaction, arg: str):
    await interaction.response.send_message(f"You said: {arg}")

@bot.slash_command( # bbq command
    name="bbq",
    description="Feed me some delicious BBQ!",
)   
async def bbq(inter: nextcord.Interaction):
    bbqEmbed = nextcord.Embed()
    bbqEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
    bbqEmbed.title = (f"BBQ fed!")
    bbqEmbed.set_thumbnail("https://cdn-icons-png.flaticon.com/512/7601/7601433.png")
    bbqEmbed.description = f'Thank you soooo much ehehe! *burp* {emotes["emoteNikkiWink"]}'
    await inter.response.send_message(embed = bbqEmbed)

# run

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")

bot.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GFQUyv.EbWFC6tB2t89qVzyyKVTqwTMWQ2dh1-t0H0Hh8")