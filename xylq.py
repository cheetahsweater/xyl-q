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
versionnum = "2.2"
updatetime = "2024/01/27 11:58"
changes = "**(2.2)** Made it so that if meme generator gets a cached message that's only one word, it repeats the word"
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

with open(f'{path}\\badid.json',"r+") as file:
    try:
        text = json.loads(file.read())
        badIDs = text
        print(badIDs)
    except JSONDecodeError as e:
        print(e)
        badIDs = {}
    file.close()

with open(f'{path}\\badcache.txt',"r+") as file:
    try:
        text = file.read()
        if len(text) > 1:
            badcacheIDs = text.split("\n")
        else:
            badcacheIDs = []
        print(badcacheIDs)
    except IndexError:
        badcacheIDs = []
    file.close()
        

mariowiki = ["https://www.mariowiki.com/index.php?title=Category:Character_artwork&fileuntil=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Back-To-School+Funny+Personality+Quiz+result+Toadette.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Black+Kirby+SSBU.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Boomgtt.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Box+Art+Background+-+Mario+Party+Island+Tour.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Captain+toad-+New+Donk+City+bg.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Club+Nintendo+Mario+German+Flag.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Daisy+MPIT.png#mw-category-media"]
stringlist = []
aff = ["Okay", "Alright", "Got it", "Affirmative"]
bots = [432610292342587392, 429305856241172480, 439205512425504771, 247283454440374274, 431544605209788416]
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
    if message.author == client.user:
        return
    if message.author.id in bots:
        return
    if len(message.content) == 0:
        return
    if str(message.channel.id) in badcacheIDs:
        return
    if str(message.author.id) in badcacheIDs:
        return
    if len(stringlist) > 100:
        stringlist = stringlist[0:20]
    else:
        stringlist.append(message.content)
    print(len(stringlist))

@client.slash_command(description="Disables message caching in a given channel or from a given user!",guild_ids=[1032727370584559617])
async def disable_cache(ctx, channel=None, user=None): 
    global badcacheIDs
    if (channel == None) and (user == None):
        await ctx.respond("Error-Q! No parameters given-Q!")
        return
    if channel != None:
        channelID = channel.strip("<>#")
        badcacheIDs.append(channelID)
        await ctx.respond(f"{random.choice(aff)}-Q! I've disabled message caching in the <#{channelID}> channel-Q!")
    if user != None:
        userID = user.strip("<>@")
        badcacheIDs.append(userID)
        await ctx.respond(f"{random.choice(aff)}-Q! I've disabled message caching for <@{userID}>-Q!")
    with open(f'{path}\\badcache.txt',"w") as file:
        for id in badcacheIDs:
            file.write(f"{id}\n")
        file.close()

@client.slash_command(description="Disables a command in a given channel!",guild_ids=[1032727370584559617])
async def disable(ctx, command: discord.Option(str, choices=["meme"]), channel): 
    global badIDs
    channelID = channel.strip("<>#")
    try:
        channelList = badIDs[command]
        channelList.append(channelID)
        badIDs.update({command:channelList})
    except KeyError:
        badIDs.update({command:[channelID]})
    with open(f'{path}\\badid.json',"w") as file:
        myJson = json.dumps(badIDs)
        file.write(myJson)
        file.close()
    await ctx.respond(f"Okay-Q! I've disabled the *{command}* command in the <#{channelID}> channel-Q!")

@client.slash_command(description="Makes a meme based on parameters given!",guild_ids=[1032727370584559617])
async def meme(ctx, top_text=None, bottom_text=None, image_link=None): 
        if (top_text == None) and (bottom_text != None):
            top_text = random.choice(stringlist)
        if (bottom_text == None) and (top_text != None):
            bottom_text = random.choice(stringlist)
        if (bottom_text == None) and (top_text == None):
            #everybody say thaaaank you chatGPT
            full_text = random.choice(stringlist)

            if " " in full_text:
                # If there are spaces, find the best place to split
                middle_index = len(full_text) // 2

                # Find the nearest space to the middle index
                split_index = middle_index
                while split_index > 0 and full_text[split_index] != " ":
                    split_index -= 1

                # If no space was found before the middle, search after the middle
                if split_index == 0:
                    split_index = middle_index
                    while split_index < len(full_text) and full_text[split_index] != " ":
                        split_index += 1

                # Split the text at the nearest space
                top_text = full_text[:split_index].strip()
                bottom_text = full_text[split_index:].strip()
            else:
                # If there are no spaces, set both to the same full_text
                top_text = full_text
                bottom_text = full_text
        if top_text != None:
            top_text_new = memeformat(top_text)
        if bottom_text != None:
            bottom_text_new = memeformat(bottom_text)
        if image_link == None:
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