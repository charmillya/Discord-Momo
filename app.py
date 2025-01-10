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
        description="View the Miralevel of a specified stylist!"
    ),
    ):
    conn = sqlite3.connect('levels.db')
    cur = conn.cursor()

    if(not user):
        cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ?', (str(inter.user.id),))
        results = cur.fetchone()
        if results is None:
            cur.execute(f'INSERT INTO users VALUES (?, ?, ?)', ((str(inter.user.id), 1, 1, 0)))
            results = (1, 1, 1)
        conn.commit()
        conn.close()
        
        if(type == 1):
            miralevelEmbed = nextcord.Embed()
            miralevelEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
            miralevelEmbed.title = (f"Stylist {inter.user.name}'s Miralevel :sparkles:")
            miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
            miralevelEmbed.add_field(name="Miralevel :sparkles:", value=str((results[2])))
            miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} xp")
            miralevelEmbed.add_field(name="Total", value=f"{str(results[1])} xp")
            await inter.response.send_message(embed = miralevelEmbed)
        else:
            await inter.response.send_message(f'Your **Mira Level :sparkles: : {results[2]}** - Level :up: in **{neededXp - results[0]} xp**! Total : **{results[1]} xp** {emoteNikkiWink}')

    else:
        cur.execute(f'SELECT xp, totalXp, level FROM users WHERE userID = ?', (str(user.id),))
        results = cur.fetchone()
        if results is None:
            cur.execute(f'INSERT INTO users VALUES (?, ?, ?)', ((str(user.id), 1, 1, 0)))
            results = (1, 1, 1)
        conn.commit()
        conn.close()
        
        if(type == 1):
            miralevelEmbed = nextcord.Embed()
            miralevelEmbed.colour = nextcord.colour.Color.from_rgb(153, 139, 46)
            miralevelEmbed.title = (f"Stylist {user.name}'s Miralevel :sparkles:")
            miralevelEmbed.set_thumbnail("https://static.wikia.nocookie.net/infinity-nikki/images/0/07/Mira_Level_Icon.png/revision/latest?cb=20241230202652")
            miralevelEmbed.add_field(name="Miralevel :sparkles:", value=str((results[2])))
            miralevelEmbed.add_field(name="Level :up: in", value=f"{str((neededXp - results[0]))} xp")
            miralevelEmbed.add_field(name="Total", value=f"{str(results[1])} xp")
            await inter.response.send_message(embed = miralevelEmbed)
        else:
            await inter.response.send_message(f"{user.name}'s **Mira Level :sparkles: : {results[2]}** - Level :up: in **{neededXp - results[0]} xp**! Total : **{results[1]} xp** {emoteNikkiWink}")

# commands

@bot.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! Momo v0.1 {emoteNikkiKiss}')

@bot.command(name="specialmessage")
async def SendMessage(ctx):
    await ctx.send(f'''# hi @everyone !! {emoteNikkiWink} \nIt's me! Yours truly **Momo** !!\n*It appears that I've been summoned here..*\n## Well, while I'm at it, I will help you with the server's daily usage !\nCharmi is still testing weird things on me and adding me all sorts of "commands".. and it appears that I'm not really stable !! So if you encounter any problem with me, reach out to Charmi !!\n\n*I might sleep at times.. and not be available ! But in that case i'll try to wake up asap! Though you'll need to give me BBQ* {emoteNikkiWink}''')

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