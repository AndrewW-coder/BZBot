import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import requests

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding = 'utf-8', mode = 'w')
intents = discord.Intents.default();
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents = intents)

def getID(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    response = requests.get(url)
    data = response.json()

    return data["id"]

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def profile(ctx, *, msg):
    await ctx.send(f"ID: {getID(msg)}")

@bot.command()
async def bz(ctx, *, msg):
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    if(response.status_code == 200):
        item = msg.upper()
        item = item.replace(' ', '_')
        data = response.json()

        ii = data["products"][item]
        
        embed = discord.Embed(title = f"{item}", description = f"Insta-Buy: {round(ii["quick_status"]["buyPrice"], 2)}\nSell Order: {round(ii["quick_status"]["sellPrice"], 2)}")
        await ctx.send(embed = embed)
    else:
        await ctx.send("Error: Invalid Input")

    

bot.run(token, log_handler = handler, log_level = logging.DEBUG)