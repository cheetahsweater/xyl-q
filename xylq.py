import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import json
from json import JSONDecodeError
import math
import random
import requests
from bs4 import BeautifulSoup

status = "Cookie Run: Ovenbreak"
#status = "Testing new features!"
versionnum = "2.3"
updatetime = "2024/01/27 14:15"
changes = "**(2.3)** Added image upload function to meme generator"
path = os.getcwd()
print(f"XyL-Q v{versionnum}")
print(updatetime)
print("womp womp")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content=True
client = commands.Bot(intents=intents)

with open(f'{path}\\secrets.txt',"r") as file:
    text = file.read()
    gapi = text.split("=")[1]

mariowiki = ["https://www.mariowiki.com/index.php?title=Category:Character_artwork&fileuntil=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Back-To-School+Funny+Personality+Quiz+result+Toadette.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Black+Kirby+SSBU.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Boomgtt.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Box+Art+Background+-+Mario+Party+Island+Tour.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Captain+toad-+New+Donk+City+bg.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Club+Nintendo+Mario+German+Flag.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Daisy+MPIT.png#mw-category-media"]
stringlist = []

imglist = []
for n in range(1,63):
    imglist.append(f"https://starmoon.neocities.org/files/gb/{n}.jpg")
for n in range(1,5):
    imglist.append(f"https://starmoon.neocities.org/files/awesomebot/grumpy/{n}.jpg")
for n in range(1,3):
    imglist.append(f"https://starmoon.neocities.org/files/awesomebot/grumpy/{n}.png")

def memeformat(text: str):
    formatlist = {
        "-":"--",
        "_":"__",
        " ":"_",
        "?":"~q",
        "&":"~a",
        "%":"~p",
        "#":"~h",
        "/":"~s",
        "\\":"~b",
        "<":"~l",
        ">":"~g",
        "\n":"~n",
        '"':"''",
        "‘":"'",
        "’":"'"
    }
    for key, value in formatlist.items():
        text = text.replace(key, value)
    return text

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    print('Bot is online!')

@client.event
async def on_message(message):
    global stringlist
    print(stringlist)
    if message.author == client.user:
        return
    if len(stringlist) > 100:
        stringlist = stringlist[0:20]
    else:
        stringlist.append(message.content)

@client.slash_command(description="Makes a meme based on parameters given!",guild_ids=[1032727370584559617])
async def meme(ctx, top_text=None, bottom_text=None, image_link=None, image_upload: discord.Attachment=None): 
        if (top_text == None) and (bottom_text != None):
            top_text = random.choice(stringlist)
        if (bottom_text == None) and (top_text != None):
            bottom_text = random.choice(stringlist)
        if (bottom_text == None) and (top_text == None):
            full_text = random.choice(stringlist)
            top_text = full_text[0:len(full_text)//2] 
            bottom_text = full_text[len(full_text)//2 if len(full_text)%2 == 0
                                            else ((len(full_text)//2)+1):] 
        if top_text != None:
            top_text_new = memeformat(top_text)
        if bottom_text != None:
            bottom_text_new = memeformat(bottom_text)
        if image_link == None:
            if image_upload != None:
                image_link = image_upload.url
            elif image_upload == None:
                numba = random.choice(range(11))
                if numba > 3:
                    words = top_text.split(" ")
                    word = f"{random.choice(words)}_{random.choice(words)}"
                    response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={gapi}&cx=25b1c3996753d4bb9&q={word}&searchType=image")
                    resultsDict = response.json()
                    results = []
                    for key, value in resultsDict.items():
                        if key == "items":
                            results = value
                    try:
                        memeImg = random.choice(results)
                        image_link = memeImg["link"]
                    except IndexError:
                        image_link = "https://mario.wiki.gallery/images/f/fe/36-Diddy_Kong.png"
                elif numba < 7:
                    image_link = random.choice(imglist)
                else:
                    url = random.choice(mariowiki)
                    reqs = requests.get(url)
                    soup = BeautifulSoup(reqs.text, 'html.parser')
                    
                    urls = []
                    for link in soup.find_all('a'):
                        url = link.get('href')
                        if url != None:
                            if url[-4:] == ".png":
                                urls.append(url)
                    page = f"https://www.mariowiki.com{random.choice(urls)}"
                    reqsagain = requests.get(page)
                    soup = BeautifulSoup(reqsagain.text, 'html.parser')
                    
                    urls = []
                    for link in soup.find_all('a'):
                        url = link.get('href')
                        if url != None:
                            if url[-4:] == ".png":
                                if "images" in url:
                                    urls.append(url)
                    image_link = random.choice(urls)
        memelink = f"https://api.memegen.link/images/custom/{top_text_new}/{bottom_text_new}.png?background={image_link}"
        await ctx.respond(memelink)

client.run(TOKEN)