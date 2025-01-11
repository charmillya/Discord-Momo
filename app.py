import nextcord
import sqlite3
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.message_content = True

#   for i in levelsFileData['user']: # test sortie de tous les utilisateurs dans levels.json avec leur xp
#       print(f"User {i['name']} - Level {i['level']} - {i['xp']} xp")

bot = commands.Bot(command_prefix = "momo ", intents=intents) # instanciation de l'objet bot

nikkisID = '1323383627492364319' # identifiant du serveur nikki's
emoteNikkiWink = "<:nikki_wink:1326685739148116009>"
emoteNikkiKiss = "<:nikki_kiss:1326589108361101405>"
emoteMiraLevel = "<:mira_level:1327334099874087043>"
emoteMiraExp = "<:mira_exp:1327333514831728720>"

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
        await message.channel.send(f":up: Congrats {message.author.mention}, you gained a **Mira Level** {emoteMiraLevel} and you are now Level **{new_level}**!")
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

    if(not user):
        cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ?', (str(inter.user.id),))
        results = cur.fetchone()
        if results is None:
            cur.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', ((str(inter.user.id), 1, 1, 1)))
            results = (1, 1, 1)
        conn.commit()
        conn.close()
        
        if(type == 1):
            miralevelEmbed = nextcord.Embed()
            miralevelEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
            miralevelEmbed.title = (f"Stylist {inter.user.name}'s Mira Level {emoteMiraLevel}")
            miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
            miralevelEmbed.add_field(name="Mira Level", value=f'{str((results[2]))} {emoteMiraLevel}')
            miralevelEmbed.add_field(name="Total", value=f"{str(results[1])} EXP {emoteMiraExp}")
            miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} EXP {emoteMiraExp}")
            await inter.response.send_message(embed = miralevelEmbed)
        else:
            await inter.response.send_message(f'Your **Mira Level {emoteMiraLevel} : {results[2]}** - Level :up: in **{neededXp - results[0]} EXP {emoteMiraExp}**! Total : **{results[1]} EXP** {emoteMiraExp} {emoteNikkiWink}')

    else:
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
            miralevelEmbed.title = (f"Stylist {user.name}'s Mira Level {emoteMiraLevel}")
            miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
            miralevelEmbed.add_field(name="Mira Level", value=f'{str((results[2]))} {emoteMiraLevel}')
            miralevelEmbed.add_field(name="Total", value=f"{str(results[1])} EXP {emoteMiraExp}")
            miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} EXP {emoteMiraExp}")
            await inter.response.send_message(embed = miralevelEmbed)
        else:
            await inter.response.send_message(f"{user.name}'s **Mira Level {emoteMiraLevel} : {results[2]}** - Level :up: in **{neededXp - results[0]} EXP {emoteMiraExp}**! Total : **{results[1]} EXP {emoteMiraExp}** {emoteNikkiWink}")

# daily outfit

@bot.slash_command(
    name="daily",
    description="Claims your daily random piece of clothing!",
)   
async def daily(
    inter: nextcord.Interaction
    ):
    conn = sqlite3.connect('momodb.db')
    cur = conn.cursor()
    cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, obtained.userid, obtained.clothid FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) LEFT OUTER JOIN obtained ON (obtained.clothid = clothes.clothid) ORDER BY RANDOM() LIMIT 1")
    results = cur.fetchone()
    selectedClothID = results[2]
    obtainedUserID = results[4]
    obtainedClothID = results[5]
    while (obtainedUserID == inter.user.id and obtainedClothID == selectedClothID):
        cur.execute("SELECT outfits.outfitname, clothes.clothid, clothes.clothname, clothes.clothimage, obtained.userid, obtained.clothid FROM clothes INNER JOIN outfits ON (outfits.outfitid = clothes.outfitid) LEFT OUTER JOIN obtained ON (obtained.clothid = clothes.clothid) ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchone()
        selectedClothID = results[2]
        obtainedUserID = results[4]
        obtainedClothID = results[5]
    cur.execute("INSERT INTO obtained VALUES (?, ?)", (inter.user.id, selectedClothID,))
    conn.commit()
    conn.close()
    dailyEmbed = nextcord.Embed()
    dailyEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
    dailyEmbed.title = (f"Your daily piece of clothing !")
    dailyEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/c/c2/Icon_Wardrobe.png/revision/latest?cb=20241222105101")
    dailyEmbed.add_field(name="Outfit", value=f'{str((results[0]))}')
    dailyEmbed.add_field(name="Name", value=f"{str(results[2])}")
    dailyEmbed.set_image(results[3])
    await inter.response.send_message(dailyEmbed)

# commands

@bot.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! Momo v0.1 {emoteNikkiKiss}')

@bot.slash_command(
    name="online",
    description="Tests if I'm online!",
)   
async def online(inter: nextcord.Interaction) -> None:
    await inter.response.send_message(f'I am alive! {emoteNikkiKiss}')

@bot.slash_command(
    name="echo",
    description="I repeat what you say!",
)  
async def echo(interaction: nextcord.Interaction, arg: str):
    await interaction.response.send_message(f"You said: {arg}")

# run

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")

bot.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GFQUyv.EbWFC6tB2t89qVzyyKVTqwTMWQ2dh1-t0H0Hh8")