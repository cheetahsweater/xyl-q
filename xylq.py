import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import json
from json import JSONDecodeError
import math
import random

status = "Cookie Run: Ovenbreak"
#status = "Testing new features!"
versionnum = "1.0"
updatetime = "2024/01/27 3:33"
changes = "**(1.0)** Created bot!!"
path = os.getcwd()
print(f"XyL-Q v{versionnum}")
print(updatetime)
print("womp womp")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content=True
client = commands.Bot(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    print('Bot is online!')

client.run(TOKEN)