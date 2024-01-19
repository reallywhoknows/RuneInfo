import os
import json
import discord
from discord.ext import commands
from colorama import Fore, Style

prefix = "!"
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=prefix, intents=intents)

with open("token.json") as content:
    file = json.load(content)

for filename in os.listdir("./extensions"):
    if filename.endswith(".py"):
        client.load_extension(f"extensions.{filename[:-3]}")
        print(Fore.GREEN + f"Extension Loaded: {filename}")
    else:
        print(Fore.RED + f"FAILED TO LOAD: {filename}")

@client.event
async def on_ready():
    print(Fore.GREEN + f"We have logged in as {client.user}" + Style.RESET_ALL)

client.run(file["token"])