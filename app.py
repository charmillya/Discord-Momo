import nextcord
intents = nextcord.Intents.default()
intents.message_content = True
from nextcord.ext import commands
from levelling import Level, LevelUpPayload

client = commands.Bot(command_prefix = "momo ", intents=intents) # instanciation de l'objet client

nikkisID = '1323383627492364319' # identifiant du serveur nikki's

# levelling system

def __init__ (client):super()
client.level = Level(client)

async def on_level_up(client, payload: LevelUpPayload):
    # This is triggered when a LevellingMember levels up
    member = payload.guild.get_member(payload.member.id)
    embed = nextcord.Embed(
        title=f"`{member.display_name}` has leveled up to level `{payload.level}`!"
    )
    await payload.channel.send(embed=embed)

async def on_message(client, message):
    leveled_up = await client.level.propagate(message)
    if leveled_up:
        await client.on_level_up(leveled_up)
    await client.process_commands(message) # visiblement là que l'exp est attribuée

# commands

@client.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! <:nikki_kiss:1326589108361101405>  Momo v0')

@client.slash_command(
    name="online",
    description="Tests if I'm online !",
)
async def online(inter: nextcord.Interaction) -> None:
    await inter.response.send_message(f'Yes I am ! <:nikki_kiss:1326589108361101405>')

@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name} - {client.user.id}")

# run

client.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GtRD0h.F09ZPTFA0MXy3g-S02F9_coreI0fPQcLexMDTo")