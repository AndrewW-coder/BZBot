import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import requests
# import base64

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
    if(response.status_code == 200):
        data = response.json()
        return data["id"]
    
def getBZ():
    url = "https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(url)
    if(response.status_code == 200):
        data = response.json()
        return data
    else:
        return -1

# def getImage(name):
#     url = f"https://api.hypixel.net/v2/resources/skyblock/items"
#     response = requests.get(url)
#     if(response.status_code == 200):
#         data = response.json()
#         image = data[name]["value"]
#         image = image.replace("\u003d", "")
#         image = base64.b64decode(image)

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
    if(getBZ() == -1):
        await ctx.send("Error: Invalid Input")
    else:
        item = msg.upper()
        item = item.replace(' ', '_')
        data = getBZ()

        ii = data["products"][item]
        
        embed = discord.Embed(title = f"{item}", description = f"Insta-Buy: {round(ii["quick_status"]["buyPrice"], 2)}\nSell Order: {round(ii["quick_status"]["sellPrice"], 2)}")
        await ctx.send(embed = embed)

@bot.command()
async def flips(ctx):
    if(getBZ() == -1):
        await ctx.send("Error: Invalid Input")
    else:
        desc = ""
        data = getBZ()
        for item in data["products"]:
            if "ENCHANTMENT" in item and "1" in item and f"{item[:-2]}_5" in data["products"]:
                ii = data["products"][item]
                # buy = round(ii["quick_status"]["buyPrice"], 2)
                sell = round(ii["quick_status"]["sellPrice"], 2)

                t5price = data["products"][f"{item[:-2]}_5"]["quick_status"]["buyPrice"]

                if(t5price < 1000000):
                    continue

                if((sell * 16)/t5price < 0.9):
                    desc += f"Item: {item} \nProfit: {round(t5price - sell * 16)}\n\n"

        embed = discord.Embed(title = "Flips", description = desc)
        await ctx.send(embed = embed)
        


    

bot.run(token, log_handler = handler, log_level = logging.DEBUG)
