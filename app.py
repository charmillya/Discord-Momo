import nextcord
import os
from nextcord.ext import commands
from assets.momoemotes import emotes
intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "!momo ", case_insensitive=True, intents=intents) # instanciation de l'objet bot

cmds = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cmds.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for cmd in cmds:
        bot.load_extension(cmd)

@bot.command(name="online?")
async def SendMessage(ctx):
    await ctx.send(f'Yes I am ! Momo v0.1 {emotes["emoteNikkiKiss"]}')

@bot.command(name="echo")
async def echo(ctx, arg: str):
    await ctx.send(f"{arg}")


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")

bot.run("MTMyNjU4Njk2MzYwMzYxOTk5NQ.GFQUyv.EbWFC6tB2t89qVzyyKVTqwTMWQ2dh1-t0H0Hh8")