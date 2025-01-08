import nextcord
import sqlite3
from nextcord.ext import commands
intents = nextcord.Intents.default()
intents.message_content = True

#   for i in levelsFileData['user']: # test sortie de tous les utilisateurs dans levels.json avec leur exp
#       print(f"User {i['name']} - Level {i['level']} - {i['exp']} exp")

bot = commands.Bot(command_prefix = "momo ", intents=intents) # instanciation de l'objet bot

nikkisID = '1323383627492364319' # identifiant du serveur nikki's

@bot.event
async def on_member_join(member): ###add a row in the db for the new member when they join
   user = member.id
   conn = sqlite3.connect('levels.db')
   cur = conn.cursor()
   cur.execute('INSERT INTO users VALUES(?, ?, ?)', (user, 0, 0))
   conn.commit()
   conn.close()
   await member.send("Your welcome message here")

# levelling system

neededExp = 50 # needed exp before levelling up

@bot.event # level system
async def on_message(message):
    user = message.author.id
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    cur.execute(f'SELECT exp, level FROM users WHERE userID = ?', (user,))
    results = cur.fetchone()

    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?)', (user, 0, 0))
        cur.execute(f'SELECT exp, level FROM users WHERE userID = ?', (user,))
        results = cur.fetchone()

    old_xp = results[0] ##the first item in the index, in this case, xp
    old_level = results[1] ## the second item in the index, in this case, level
    new_xp = old_xp + 1
    if new_xp == neededExp: #this is where you set the threshold for leveling up to the first level
        new_level = old_level+1
        new_xp = 0
        await message.channel.send(f"Congratulations {message.author.mention}, you gained a **Mira Level** :sparkles: and you are now Level **{new_level}**!")
    else:
        new_level = old_level
    ###add more logic here for successive level-ups
    cur.execute('UPDATE users SET exp = ?, level = ? WHERE userid = ?', (new_xp, new_level, user))
    conn.commit()
    conn.close()
    await bot.process_commands(message)

@bot.slash_command( # check level and exp remaining
    name="miralevel",
    description="Lets you know your Mira Level and remaining exp before levelling up!",
)   
async def miralevel(inter: nextcord.Interaction):
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()
    cur.execute(f'SELECT exp, level FROM users WHERE userID = ?', (str(inter.user.id),))
    results = cur.fetchone()
    if results is None:
        cur.execute(f'INSERT INTO users VALUES (?, ?, ?)', ((str(inter.user.id), 0, 0)))
        cur.execute(f'SELECT exp, level FROM users WHERE userID = ?', (str(inter.user.id),))
        results = cur.fetchone()
    conn.commit()
    conn.close()
    await inter.response.send_message(f'Your **Mira Level :sparkles: : {results[1]}** - **{neededExp - results[0]} exp remaining** until next level! <:nikki_wink:1326685739148116009>')

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

bot.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GtRD0h.F09ZPTFA0MXy3g-S02F9_coreI0fPQcLexMDTo")