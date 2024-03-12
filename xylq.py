import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from traceback import format_exc
import os
import json
from json import JSONDecodeError
import math
import random
import requests
from bs4 import BeautifulSoup
import asyncio

status = "Cookie Run: Ovenbreak"
#status = "Testing new features!"
versionnum = "3.9a"
updatetime = "2024/03/11 20:48"
changes = "**(3.9)** Added error handling for Mudae error, improved general error handling, added logs to message indexing to diagnose meme command bug\n(a) Fixed bug with message indexing logs"
path = os.getcwd()
print(f"XyL-Q v{versionnum}")
print(updatetime)
print("womp womp")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content=True
client = commands.Bot(intents=intents)

#Load Google API key
with open(f'{path}\\secrets.txt',"r") as file:
    text = file.read()
    gapi = text.split("=")[1]

#Load individual user-to-user reputation database
with open(f'{path}\\rep.json',"r+") as file:
    try:
        text = json.loads(file.read())
        rep = text
    except JSONDecodeError as e:
        print(e)
        rep = {}
    file.close()

#Load user total reputation database
with open(f'{path}\\totalrep.json',"r+") as file:
    try:
        text = json.loads(file.read())
        totalrep = text
    except JSONDecodeError as e:
        print(e)
        totalrep = {}
    file.close()

#Load list of channels in which certain commands are disabled
with open(f'{path}\\badid.json',"r+") as file:
    try:
        text = json.loads(file.read())
        badIDs = text
    except JSONDecodeError as e:
        print(e)
        badIDs = {}
    file.close()

#Load list of loved Mudae characters
with open(f'{path}\\lovelist.json',"r+") as file:
    try:
        text = json.loads(file.read())
        lovelist = text
    except JSONDecodeError as e:
        print(e)
        lovelist = {}
    file.close()

#Load list of loved Mudae sources
with open(f'{path}\\sourcelist.json',"r+") as file:
    try:
        text = json.loads(file.read())
        sourcelist = text
    except JSONDecodeError as e:
        print(e)
        sourcelist = {}
    file.close()


#Load list of channels in which message caching is disabled
with open(f'{path}\\badcache.txt',"r+") as file:
    try:
        text = file.read()
        if len(text) > 1:
            badcacheIDs = text.split("\n")
        else:
            badcacheIDs = []
    except IndexError:
        badcacheIDs = []
    file.close()

#Load list of guilds
with open(f'{path}\\guilds.txt',"r+") as file:
    try:
        text = file.read()
        if len(text) > 1:
            guilds = text.split("\n")
            for serverID in guilds:
                serverID = int(serverID)
        else:
            print("Error! Guilds not loaded!")
            guilds = []
    except IndexError:
        print("Error! Guilds not loaded!")
    file.close()

#List of possible wikis that meme command can grab images from        
wikis = ["mario","minecraft","ssb","cookierun","logo"]

#List of image pages from each wiki (ideally this will be replaced with something that just grabs all of the possible ones instead of this mess)
mariowiki = ["https://www.mariowiki.com/index.php?title=Category:Character_artwork&fileuntil=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=AlolanExeggutorUltimate.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Back-To-School+Funny+Personality+Quiz+result+Toadette.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Black+Kirby+SSBU.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Boomgtt.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Box+Art+Background+-+Mario+Party+Island+Tour.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Captain+toad-+New+Donk+City+bg.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Club+Nintendo+Mario+German+Flag.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Daisy+MPIT.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Ditrani+Salvatore+MRSOH+Midnite.jpg#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DKC2+Screech.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DMW+Skill+Summit+12+mentors.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Donkey+Kong+vector+art.svg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DrMarioLesson.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Fire+Mario.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=FSWaluigi.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Goboten+Perfect.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Happy+Holidays+Greeting+Card+Poll+preview.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=ITnKnBT+NOM+Manga+Program+3+8.jpg#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Kiddy+Kong+running+DKC3+artwork.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Koopa+Troopa+and+Paratroopa+-+MKDD.png#mw-category-media"]

mcwiki = ["https://minecraft.wiki/w/Category:Mojang_images","https://minecraft.wiki/w/Category:Mojang_images?filefrom=1-18-dripstone-caves.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=1.19.1-pre3.jpg#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=11a-44.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=14w31a+textures+0.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=2+joined+shipwrecks.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=21a01-25.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=3inone.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Abominable+Weaver+Icon.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Acacia+Sign+JE1+BE1.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Adriene+Texture+%28MCD%29.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Albino+Cow+Spawn+Egg+Icon.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Allay+animated+sticker.gif#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Alpha+v1.2.1.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Ancient+City+intact+corner+wall+1.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Anti+Mortar.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Area+render.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Armored+Jungle+Zombie.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Astatine.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Attached+Stem+Age+10+%28S%29+JE1.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Autoreset+booster.jpg#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Baby+Brown+Horse+Revision+2.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Baby+Light+Blue+Sheep+JE1.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Baby+Yellow+Sheep+JE3.png#mw-category-media",
          ]

ssb = ["https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230614074616&limit=500",
       "https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230211232543&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230126182127&limit=500",
       "https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20211005224641&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20210703010151&limit=500"]

cb = ["https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230822035355&limit=500",
      "https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230207164344&limit=500","https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20220819144935&limit=500",
      "https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20211027050918&limit=500","https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20210220074319&limit=500",
      "https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20191207025325&limit=500","https://carebears.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20181118235504&limit=500"]

cr = ["https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://cookierun.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

crk = ["https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://cookierunkingdom.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

logo = ["https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240209233655&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240205205824&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240203005106&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240131171306&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240128142929&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240125220604&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240123193140&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240120203521&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240117080417&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240113151603&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240113151603&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240106011557&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20240103153155&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231230225259&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228013637&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231223221351&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231221191611&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231219172320&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231217123726&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231214070528&limit=500",
        "https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231210201418&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231207134742&limit=500","https://logos.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231203005443&limit=500"]

stringlist = {} #I don't remember what this even is
aff = ["Okay", "Alright", "Got it", "Affirmative","Sounds good"] #Different affirmative phrases the bot can say when asked to do something
selfrep = ["You're giving reputation to me-Q?? Well, thank you-Q! ^^","Oh...thank you so much for the reputation-Q! I will take good care of it-Q! ^^"] #Cutie little guy messages for when reputation is awarded to XyL-Q
bots = [429305856241172480, 439205512425504771, 247283454440374274, 431544605209788416] #Bot IDs so XyL-Q can avoid indexing their messages
imglist = [] #Instantiating list for later

#The API I use for the meme creation has a lot of character substitution involved so this is a command that does all of that automatically
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
        "’":"'",
        "“":'"',
        "”":'"'
    }
    for key, value in formatlist.items():
        text = text.replace(key, value)
    return text

#Changes bot's status and announces (to me) that it's online
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    global report 
    report = client.get_channel(1213349040050409512)
    print('Bot is online!')

#Reputation giving and removing function
@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    try:
        if reaction.emoji == "🏅": #Might add all the other medal emojis too just for funsies
            #Heavily revised by ChatGPT which was not necessarily what I even wanted it to do
            guild_id_str = str(reaction.message.guild.id)
            user_id_str = str(user.id)
            author_id_str = str(reaction.message.author.id)

            # Check for self-reputation or specific user ID conditions
            if reaction.message.author == client.user:
                await reaction.message.channel.send(random.choice(selfrep))
            elif author_id_str == "1204234942897324074":
                await reaction.message.channel.send("My apologies, but I cannot handle giving reputation to tuppers-Q!")
                return  # Exit for specific user conditions
            elif user_id_str == author_id_str:
                await reaction.message.channel.send("My apologies, but I cannot let you give reputation to yourself-Q!")
                return  # Exit to prevent self-reputation

            # Ensure guild dictionary exists
            if guild_id_str not in rep:
                rep[guild_id_str] = {}
            if user_id_str not in rep[guild_id_str]:
                rep[guild_id_str][user_id_str] = {}
            if author_id_str not in rep[guild_id_str][user_id_str]:
                rep[guild_id_str][user_id_str][author_id_str] = 0

            # Update rep
            rep[guild_id_str][user_id_str][author_id_str] += 1
            await report.send(f"Reputation given to {author_id_str} by {user_id_str} updated. It is now {rep[guild_id_str][user_id_str][author_id_str]}")

            # Ensure totalrep structure exists
            if guild_id_str not in totalrep:
                totalrep[guild_id_str] = {}
            if author_id_str not in totalrep[guild_id_str]:
                totalrep[guild_id_str][author_id_str] = 0

            # Update totalrep
            totalrep[guild_id_str][author_id_str] += 1
            await report.send(f"Total reputation of {author_id_str} updated. It is now {totalrep[guild_id_str][author_id_str]}")
        

            await reaction.message.channel.send(f"<@{user_id_str}> has given <@{author_id_str}> +1 reputation-Q!")

            # Write to files
            with open(f'{path}\\rep.json', "w") as file:
                json.dump(rep, file)
            
            with open(f'{path}\\totalrep.json', "w") as file:
                json.dump(totalrep, file)
        if reaction.emoji == "🍅":
            guild_id_str = str(reaction.message.guild.id)
            user_id_str = str(user.id)
            author_id_str = str(reaction.message.author.id)

            if reaction.message.author == client.user:
                await reaction.message.channel.send("I will not permit uncleanliness on my person-Q!!")
                return

            # Check for self-reputation or specific user ID conditions
            if reaction.message.author == client.user:
                await reaction.message.channel.send(random.choice(selfrep))
            elif author_id_str == "1204234942897324074":
                await reaction.message.channel.send("My apologies, but I cannot handle taking reputation from tuppers-Q!")
                return  # Exit for specific user conditions
            elif user_id_str == author_id_str:
                await reaction.message.channel.send("Why would you want to take away your own rep-Q?!")
                return  # Exit to prevent self-reputation

            # Ensure guild dictionary exists
            if guild_id_str not in rep:
                rep[guild_id_str] = {}
            if user_id_str not in rep[guild_id_str]:
                rep[guild_id_str][user_id_str] = {}
            if author_id_str not in rep[guild_id_str][user_id_str]:
                rep[guild_id_str][user_id_str][author_id_str] = 0

            # Update rep
            rep[guild_id_str][user_id_str][author_id_str] -= 1
            await report.send(f"Reputation given to {author_id_str} by {user_id_str} updated. It is now {rep[guild_id_str][user_id_str][author_id_str]}")

            # Ensure totalrep structure exists
            if guild_id_str not in totalrep:
                totalrep[guild_id_str] = {}
            if author_id_str not in totalrep[guild_id_str]:
                totalrep[guild_id_str][author_id_str] = 0
                await reaction.message.channel.send("This user has no rep to take away-Q!")
            if totalrep[guild_id_str][author_id_str] <= 0:
                totalrep[guild_id_str][author_id_str] = 0
                await reaction.message.channel.send("This user has no rep to take away-Q!")
            else:
                # Update totalrep
                totalrep[guild_id_str][author_id_str] -= 1
                await report.send(f"Total reputation of {author_id_str} updated. It is now {totalrep[guild_id_str][author_id_str]}")

                await reaction.message.channel.send(f"<@{user_id_str}> threw a tomato at <@{author_id_str}>-Q! Rather unclean of you-Q…")

            # Write to reputation databases
            with open(f'{path}\\rep.json', "w") as file:
                json.dump(rep, file)
            
            with open(f'{path}\\totalrep.json', "w") as file:
                json.dump(totalrep, file)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {reaction.message.guild.name}")
    
#Message indexing for meme command with no parameters
@client.event
async def on_message(message: discord.Message):
    try:
        global stringlist
        if message.author == client.user: #Obviously don't index XyL-Q's own messages
            return
        if message.author.id in bots: #Don't index certain bots (probably going to revise this because it's kind of janky)
            return
        if message.author.id == 432610292342587392: #Mudae notification logic
            if len(message.embeds) == 1:
                sourcelines = message.embeds[0].description.split("\n")[:-1]
                source = ""
                for line in sourcelines:
                    source += f"{line} "
                try:
                    roll = {message.embeds[0].author.name.casefold():source.strip().casefold()}
                except AttributeError:
                    return
                for userlist in lovelist.items():
                    for entry in dict(userlist[1]).items():
                        if roll == {entry[0]:entry[1]}:
                            await message.channel.send(f"{entry[0]} is loved by <@{userlist[0]}>-Q!")
                for user, userlist in sourcelist.items():
                    for usersource in userlist:
                        if usersource.strip().casefold() == source.strip().casefold():
                            await message.channel.send(f"{usersource} is loved by <@{user}>-Q!")

        if len(message.content) == 0: #Don't index messages with no text in them (e.g. files or images)
            return
        if str(message.channel.id) in badcacheIDs: #Don't index messages from channels that are in the "don't index these" list
            return
        if str(message.author.id) in badcacheIDs: #Don't index messages from users that are in the "don't index these" list
            return
        if "||" in message.content: #Don't index messages with spoiler tags in them
            return
        else:
            try:
                msglist = stringlist[str(message.guild.id)] #Grabs the list of already indexed messages for the server the message is in

                if len(msglist) > 100: #Index list should always be less than 100 just to make sure the little guy doesn't get too overwhelmed
                    for x in range(70):
                        prevlength = len(msglist)
                        msglist.pop(0) #Delete the oldest 70 messages from the list, I can't remember if this deletes the recent ones accidentally
                        report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                        msglist.append(message.content)
                        report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                else:
                    prevlength = len(msglist)
                    msglist.append(message.content)
                    report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                stringlist[str(message.guild.id)] = msglist #Update the dictionary of indexed messages per server
            except KeyError:
                exceptionstring = format_exc()
                await report.send(f"{exceptionstring}")
            stringlist.update({str(message.guild.id): [message.content]}) #Adds a new entry to the dictionary if there's no indexed messages for the server
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {message.guild.name}")

#Mainly I just use this to make sure I'm running the latest version after I update him
@client.slash_command(description="Returns XyL-Q version number!", guild_ids=guilds)
async def version(ctx: discord.Interaction): 
    await ctx.respond(f"Hello-Q! I'm XyL-Q, running version {versionnum} released on {updatetime}-Q!\n\n__Changelog__\n{changes}")

#Simple way for users to check reputation, also revised by ChatGPT even though I didn't ask it to revise this either
@client.slash_command(description="Shows you your reputation and other related stats!")
async def reputation(ctx: discord.Interaction):
    try:
        guild_id_str = str(ctx.guild.id)
        user_id_str = str(ctx.author.id)

        embed = discord.Embed(title=f"{ctx.author.display_name}'s reputation stats-Q!",
                            color=ctx.author.color)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        # Adjusting for guild-specific total reputation
        guild_totalrep = totalrep.get(guild_id_str, {})
        user_total_rep = guild_totalrep.get(user_id_str, 0)
        embed.add_field(name="Total reputation:", value=str(user_total_rep))

        # Adjusting for guild-specific given reputation details
        guild_rep = rep.get(guild_id_str, {})
        user_rep = guild_rep.get(user_id_str, {})

        # Handling the display for rep given
        given_rep_str = ""
        if user_rep:
            # Sort by amount of rep given, descending
            sorted_given_rep = sorted(user_rep.items(), key=lambda x: x[1], reverse=True)
            for target_user_id, amount in sorted_given_rep[:3]:  # Get top 3
                given_rep_str += f"<@{target_user_id}>: {amount} rep\n"
        given_rep_str = given_rep_str or "Nobody! Does your selfishness know no bounds?!"
        embed.add_field(name="You've given the most rep to:", value=given_rep_str, inline=False)

        # Adjusting for guild-specific received reputation details
        received_rep_str = ""
        for giver_id, given_to in guild_rep.items():
            if user_id_str in given_to:
                received_rep_str += f"<@{giver_id}>: {given_to[user_id_str]} rep\n"

        received_rep_str = received_rep_str or "Nobody...I'd give you rep if I could, though :("
        embed.add_field(name="You've received the most rep from:", value=received_rep_str, inline=False)

        await ctx.respond(embed=embed)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Disable caching for given channel or user
@client.slash_command(description="Disables message caching in a given channel or from a given user!", guild_ids=guilds)
async def disable_cache(ctx: discord.Interaction, channel: str=None, user: str=None): 
    try:
        global badcacheIDs
        if (channel == None) and (user == None):
            await ctx.respond("Error-Q! No parameters given-Q!")
            return
        if channel != None:
            channelID = channel.strip("<>#") #Remove the non-number characters present in a Discord channel ping
            badcacheIDs.append(channelID)
            await ctx.respond(f"{random.choice(aff)}-Q! I've disabled message caching in the <#{channelID}> channel-Q!")
        if user != None:
            userID = user.strip("<>@") #Remove the non-number characters present in a Discord user ping
            badcacheIDs.append(userID)
            await ctx.respond(f"{random.choice(aff)}-Q! I've disabled message caching for <@{userID}>-Q!")
        #Save new list to database
        with open(f'{path}\\badcache.txt',"w") as file:
            for id in badcacheIDs:
                file.write(f"{id}\n")
            file.close()
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Disables a command's use in a certain channel, not really even sure what the use case for this is
@client.slash_command(description="Disables a command in a given channel!", guild_ids=guilds)
async def disable(ctx: discord.Interaction, command: discord.Option(str, choices=["meme", "reputation", "version"]), channel: str): 
    try:
        global badIDs
        channelID = channel.strip("<>#") #Remove the non-number characters present in a Discord channel ping
        try:
            #Add channel to list of no-no channels for command
            channelList = badIDs[command]
            channelList.append(channelID)
            badIDs.update({command:channelList})
        except KeyError:
            exceptionstring = format_exc()
            await report.send(f"{exceptionstring}")
            #Add new entry for the given command if not present
            badIDs.update({command:[channelID]})
        #Save new list to database
        with open(f'{path}\\badid.json',"w") as file:
            myJson = json.dumps(badIDs)
            file.write(myJson)
            file.close()
        await ctx.respond(f"Okay-Q! I've disabled the *{command}* command in the <#{channelID}> channel-Q!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Utility for Mudae rolls, notifies a user of any character given with this command
@client.slash_command(description="Loves a character from Mudae to notify you later if that character is rolled!", guild_ids=guilds)
async def love_character(ctx: discord.Interaction, character: str, source: str, user: str=None):
    try:
        if user == None:
            IDstring = str(ctx.author.id)
        else:
            IDstring = user.strip("<>@")
        try:
            userlovelist = lovelist[IDstring]
        except KeyError:
            userlovelist = {}
        userlovelist[character.casefold().strip()] = source.casefold().strip()
        lovelist[IDstring] = userlovelist
        with open(f'{path}\\lovelist.json', "w") as file:
            json.dump(lovelist, file)
        if user != None:
            guild: discord.Guild = ctx.guild
            member: discord.User = await guild.fetch_member(int(IDstring))
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {character} from {source} to {member.display_name}'s love list-Q!")
        else:
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {character} from {source} to your love list-Q!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")
    
#Utility for Mudae rolls, notifies a user of any character from the source given with this command
@client.slash_command(description="Loves a source from Mudae to notify you later if any character from that source is rolled!", guild_ids=guilds)
async def love_source(ctx: discord.Interaction, source: str, user: str=None):
    try:
        if user == None:
            IDstring = str(ctx.author.id)
        else:
            IDstring = user.strip("<>@")
        try:
            usersourcelist = sourcelist[IDstring]
        except KeyError:
            usersourcelist = []
        usersourcelist.append(source.casefold().strip())
        sourcelist[IDstring] = usersourcelist
        with open(f'{path}\\sourcelist.json', "w") as file:
            json.dump(sourcelist, file)
        if user != None:
            guild: discord.Guild = ctx.guild
            member: discord.User = await guild.fetch_member(int(IDstring))
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {source} to {member.display_name}'s love list-Q!")
        else:
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {source} to your love list-Q!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#MY MAGNUM OPUS (the meme command)
@client.slash_command(description="Makes a meme based on parameters given!", guild_ids=guilds)
async def meme(ctx: discord.Interaction, top_text: str=None, bottom_text: str=None, image_link: str=None, image_upload: discord.Attachment=None, wiki: discord.Option(str, choices=wikis)=None): 
    try:
        if (top_text == None) and (bottom_text != None):
            top_text = bottom_text
        if (bottom_text == None) and (top_text != None):
            bottom_text = top_text
        #This specific little section was given to us by ChatGPT because it was too hard for me to do it
        if (bottom_text == None) and (top_text == None):
            try:
                full_text = random.choice(stringlist[str(ctx.guild.id)])
            except Exception as e:
                exceptionstring = format_exc()
                await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")
                full_text = "no messages indexed"

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
        #Formats the text as necessary for the meme generator API thing
        if top_text != None:
            top_text_new = memeformat(top_text)
        if bottom_text != None:
            bottom_text_new = memeformat(bottom_text)
        #If there's no image link given, pick a random one from the choice of a few different wikis
        if image_link == None:
            #Obviously if there's an image upload then it doesn't really matter that there's no image link
            if image_upload != None:
                await ctx.response.defer()
                image_link = image_upload.url #This is currently broken for whatever reason, working on trying to mirror images to another site
            elif image_upload == None:
                numba = random.choice(range(11))
                if numba > 10:
                    #Chooses two random words from the string and Googles them in order to find an image
                    words = top_text.split(" ")
                    word = f"{random.choice(words)}_{random.choice(words)}"
                    await ctx.response.defer()
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
                        exceptionstring = format_exc()
                        await report.send(f"<@120396380073099264>\n{exceptionstring}")
                        image_link = "https://mario.wiki.gallery/images/f/fe/36-Diddy_Kong.png"
                #elif numba < 1:
                    #This list is empty right now so once I populate that list I'll add this back in
                    #image_link = random.choice(imglist)
                else:
                    if wiki == None:
                        wiki = random.choice(wikis)

                    #Definitely going to move this to a function ASAP because this code is ridiculously long and it's all the same
                    #Once I move it to a function I will add comments but for now it would be extremely redundant lol
                    if wiki == "mario":
                        url = random.choice(mariowiki)
                        await ctx.response.defer()
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
                        try:
                            image_link = random.choice(urls)   
                        except IndexError:
                            page = f"https://www.mariowiki.com{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = random.choice(urls)   
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://i1.wp.com/files.polldaddy.com/9b53a5da9af99125866e48003cce5675-65c92e58a003b.jpg"
                                
                    if wiki == "minecraft":
                        url = random.choice(mcwiki)
                        await ctx.response.defer()
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "w/File:" in url:
                                        urls.append(url)
                        page = f"https://minecraft.wiki{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    if "images" in url:
                                        urls.append(url)
                        try:
                            image_link = f"https://minecraft.wiki{random.choice(urls)}"
                        except IndexError:
                            page = f"https://minecraft.wiki{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = f"https://minecraft.wiki{random.choice(urls)}" 
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://static.wikia.nocookie.net/logopedia/images/4/43/Sat.1_montage_-_by_Nico234.png"

                    if wiki == "ssb":
                        url = url = random.choice(ssb)
                        await ctx.response.defer()
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "File:" in url:
                                        urls.append(url)
                        page = f"https://supersmashbros.fandom.com{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    #print(url)
                                    if "images" in url:
                                        urls.append(url)
                        try:
                            image_link = random.choice(urls)   
                        except IndexError:
                            exceptionstring = format_exc()
                            await report.send(f"{exceptionstring}")
                            page = f"https://supersmashbros.fandom.com{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = random.choice(urls)   
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://static.wikia.nocookie.net/ssb/images/3/39/Super-Smash-Bros.-Ultimate-OFFICIAL-Key-Art-Wide-by-.jpg/"

                    if wiki == "cb":
                        url = url = random.choice(cb)
                        await ctx.response.defer()
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "File:" in url:
                                        urls.append(url)
                        page = f"https://carebears.fandom.com{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    #print(url)  
                                    if "images" in url:
                                        urls.append(url)
                        try:
                            image_link = random.choice(urls)   
                        except IndexError:
                            exceptionstring = format_exc()
                            await report.send(f"{exceptionstring}")
                            page = f"https://carebears.fandom.com{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = random.choice(urls)   
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://static.wikia.nocookie.net/carebears/images/3/30/Flower_Power_Bear_UTM.png"
                                
                    if wiki == "cookierun":
                        url = url = random.choice(cr)
                        await ctx.response.defer()
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "File:" in url:
                                        urls.append(url)
                        page = f"https://cookierun.fandom.com{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    #print(url)
                                    if "images" in url:
                                        urls.append(url)
                        try:
                            image_link = random.choice(urls)   
                        except IndexError:
                            exceptionstring = format_exc()
                            await report.send(f"{exceptionstring}")
                            page = f"https://cookierun.fandom.com{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = random.choice(urls)   
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://static.wikia.nocookie.net/8942cb43-4ab3-498a-b9af-860b7743a226/"
                    if wiki == "logo":
                        url = url = random.choice(logo)
                        await ctx.response.defer()
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "File:" in url:
                                        urls.append(url)
                        page = f"https://logos.fandom.com{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    #print(url)
                                    if "images" in url:
                                        urls.append(url)
                        try:
                            image_link = random.choice(urls)   
                        except IndexError:
                            exceptionstring = format_exc()
                            await report.send(f"<@120396380073099264>\n{exceptionstring}")
                            page = f"https://logos.fandom.com{random.choice(urls)}"
                            reqsagain = requests.get(page)
                            soup = BeautifulSoup(reqsagain.text, 'html.parser')
                            
                            urls = []
                            for link in soup.find_all('a'):
                                url = link.get('href')
                                if url != None:
                                    if ".png" in url:
                                        #print(url)
                                        if "images" in url:
                                            urls.append(url)
                                try:
                                    image_link = random.choice(urls)   
                                except IndexError:
                                    exceptionstring = format_exc()
                                    await report.send(f"<@120396380073099264>\n{exceptionstring}")
                                    image_link = "https://static.wikia.nocookie.net/logopedia/images/4/43/Sat.1_montage_-_by_Nico234.png"
        memelink = f"https://api.memegen.link/images/custom/{top_text_new}/{bottom_text_new}.png?background={image_link}"
        await ctx.followup.send(content=memelink)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}")

client.run(TOKEN)