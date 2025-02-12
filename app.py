import nextcord
import os
from datetime import datetime
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from assets.momoemotes import emotes
intents = nextcord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix = "!momo ", case_insensitive=True, intents=intents,status=nextcord.Status.idle, activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Together Till Infinity!")) # instanciation de l'objet bot

cmds = []
load_dotenv()

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
async def echo(ctx, *,args):
    if ctx.message.author.id in [593889874315182133, 505101653536669697]:
        await ctx.send(args)
        await ctx.message.delete()
    else:
        await None

@bot.command(name="allservers")
async def PrintAllServers(ctx):
    counter = 0
    for guild in bot.guilds:
        counter += 1
        print(guild.name)
    print("_______________________________________________________________")
    print(f"TOTAL: {counter} servers")
    await ctx.send(f"TOTAL: {counter} servers")
    print("_______________________________________________________________")

@bot.command(name="allmembers")
async def PrintAllMembers(ctx):
    counterMembers = 0
    counterServers = 0
    for guild in bot.guilds:
        counterServers += 1
        print("_______________________________________________________________")
        print(f"GUILD {guild.name}")
        print("_______________________________________________________________")
        for member in guild.members:
            counterMembers += 1
            print(member.name)
    print("_______________________________________________________________")
    print(f"TOTAL: {counterMembers} members in {counterServers} servers")
    await ctx.send(f"TOTAL: {counterMembers} members in {counterServers} servers")
    print("_______________________________________________________________")

@bot.event
async def on_ready():
    print("_______________________________________________________________")
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")
    print("_______________________________________________________________")

bot.run(os.getenv('TOKEN'))