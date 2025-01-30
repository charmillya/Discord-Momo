import nextcord
import os
import asyncio
import sqlite3
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

@bot.command(name="test")
async def SendMessage(ctx):
    if ctx.message.author.id in [593889874315182133, 505101653536669697]:
        await ctx.send(ctx.guild.id)
    else:
        await None

@bot.event
async def on_ready():
    print("_______________________________________________________________")
    print(f"Logged in as: {bot.user.name} - {bot.user.id}")
    print("_______________________________________________________________")

bot.run(os.getenv('TOKEN'))