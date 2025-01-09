import nextcord
import sqlite3
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.message_content = True

#   for i in levelsFileData['user']: # test sortie de tous les utilisateurs dans levels.json avec leur xp
#       print(f"User {i['name']} - Level {i['level']} - {i['xp']} xp")

bot = commands.Bot(command_prefix = "momo ", intents=intents) # instanciation de l'objet bot

nikkisID = '1323383627492364319' # identifiant du serveur nikki's

# levelling system

neededXp = 50 # needed xp before levelling up

@bot.event # level system
async def on_message(message):
    user = message.author.id
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    cur.execute(f'SELECT xp, level FROM users WHERE userID = ?', (user,))
    results = cur.fetchone()

    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?, ?)', (user, 1, 0, 0))
        cur.execute(f'SELECT xp, level FROM users WHERE userID = ?', (user,))
        results = cur.fetchone()

    old_xp = results[0] ##the first item in the index, in this case, xp
    old_level = results[1] ## the second item in the index, in this case, level
    perm_xp = old_xp + 1
    new_xp = old_xp + 1
    if new_xp == neededXp: #this is where you set the threshold for leveling up to the first level
        new_level = old_level+1
        new_xp = 0
        await message.channel.send(f":up: Congrats {message.author.mention}, you gained a **Mira Level** :sparkles: and you are now Level **{new_level}**!")
    else:
        new_level = old_level
    ###add more logic here for successive level-ups
    cur.execute('UPDATE users SET xp = ?, totalXp = ?, level = ? WHERE userid = ?', (new_xp, perm_xp, new_level, user))
    conn.commit()
    conn.close()
    await bot.process_commands(message)

@bot.slash_command( # check level and xp remaining
    name="miralevel",
    description="Lets you know your Mira Level and remaining xp before levelling up!",
)   
async def miralevel(inter: nextcord.Interaction):
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ?', (str(inter.user.id),))
    results = cur.fetchone()
    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?)', ((str(inter.user.id), 1, 1, 0)))
        results = (1, 1, 1)
    conn.commit()
    conn.close()
    
    miralevelEmbed = nextcord.Embed()
    # ajouter thumbnail etc
    miralevelEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
    miralevelEmbed.title = (f"Stylist {inter.user.name}'s Miralevel :sparkles:")
    miralevelEmbed.add_field(name="Miralevel :sparkles:", value=str(results[2]))
    miralevelEmbed.add_field(name="Level :up: in", value=str(neededXp - results[0]))
    miralevelEmbed.add_field(name="Total XP", value=str(results[1]))
    await inter.response.send_message(embed = miralevelEmbed)
    # faire une slash cmd a deux choix : embed envoie l'embed sinon si option pas choisie envoie ligne
    #await inter.response.send_message(f'Your **Mira Level :sparkles: : {results[2]}** - Level :up: in **{neededXp - results[0]} xp**! Total : **{results[1]} xp** <:nikki_wink:1326685739148116009>')

# commands

@bot.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! <:nikki_kiss:1326589108361101405>  Momo v0')

@bot.slash_command(
    name="online",
    description="Tests if I'm online!",
)   
async def online(inter: nextcord.Interaction) -> None:
    await inter.response.send_message(f'I am alive! <:nikki_kiss:1326589108361101405>')

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")

# run

bot.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GFQUyv.EbWFC6tB2t89qVzyyKVTqwTMWQ2dh1-t0H0Hh8")