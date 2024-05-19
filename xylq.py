from datetime import datetime
import discord
from discord.ext import commands
from discord.utils import get
from discord.errors import Forbidden
from dotenv import load_dotenv
from traceback import format_exc
import os
import json
from json import JSONDecodeError
import random
import requests
from bs4 import BeautifulSoup
import asyncio
import pytz

#status = "Cookie Run: Witch’s Castle"
status = "Testing new features!"
versionnum = "5.3"
updatetime = "2024/05/19 12:13"
changes = "**(5.3)** Updated reminder function to not require date and fixed AM time handling and 12PM bug"
path = os.getcwd()
print(f"XyL-Q v{versionnum}")
print(updatetime)
print("womp womp")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TOKEN = os.getenv('TEST_TOKEN')
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

#Load list of reminders
with open(f'{path}\\reminders.json',"r+") as file:
    try:
        text = json.loads(file.read())
        reminders = text
    except JSONDecodeError as e:
        print(e)
        reminders = {}
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
wikis = ["Mario","Minecraft","Super Smash Bros.","Cookie Run", "Regretevator", "Undertale AUs", "Roblox",
         "Vocaloid", "NiGHTS", "My Singing Monsters", "PHIGHTING!", "Fortnite", "Animal Crossing", "Hazbin Hotel",
         "Urusei Yatsura"]

backup_img = ["https://files.catbox.moe/5k42ay.jpg", "https://files.catbox.moe/blscgw.jpg", "https://files.catbox.moe/p4d6xv.png",
              "https://lastfm.freetls.fastly.net/i/u/770x0/d1761236c12379d3e1dfce76023231f6.jpg","https://lastfm.freetls.fastly.net/i/u/770x0/9f06d6f7dc349a246a9d70127b9ad070.jpg",
              "https://lastfm.freetls.fastly.net/i/u/770x0/4386a469e620103f8436b3e969075959.jpg","https://lastfm.freetls.fastly.net/i/u/770x0/73b95651e23dd27638bed35eb12ccdd0.jpg",
              "https://lastfm.freetls.fastly.net/i/u/770x0/5c50b8fb0d6073befc75e62e3aa938cf.jpg","https://lastfm.freetls.fastly.net/i/u/770x0/9ab8ee8d7a7ff8bfb0c00afb89a38c16.jpg",
              "https://lastfm.freetls.fastly.net/i/u/770x0/0845c2a12bafb49cd9a6ffa8dbbb2978.jpg"]

common_timezones = [
    "Etc/GMT+12",   # GMT-12
    "Pacific/Midway",  # GMT-11
    "Pacific/Honolulu",  # GMT-10
    "America/Anchorage",  # GMT-9
    "America/Los_Angeles",  # GMT-8
    "America/Denver",  # GMT-7
    "America/Chicago",  # GMT-6
    "America/New_York",  # GMT-5
    "America/Caracas",  # GMT-4
    "America/Sao_Paulo",  # GMT-3
    "Atlantic/Cape_Verde",  # GMT-2
    "Atlantic/Azores",  # GMT-1
    "UTC",  # GMT+0
    "Europe/London",  # GMT+1
    "Europe/Paris",  # GMT+2
    "Europe/Moscow",  # GMT+3
    "Asia/Dubai",  # GMT+4
    "Asia/Karachi",  # GMT+5
    "Asia/Dhaka",  # GMT+6
    "Asia/Bangkok",  # GMT+7
    "Asia/Hong_Kong",  # GMT+8
    "Asia/Tokyo",  # GMT+9
    "Australia/Sydney",  # GMT+10
    "Pacific/Noumea"  # GMT+11
]

months = ['January',
 'February',
 'March',
 'April',
 'May',
 'June',
 'July',
 'August',
 'September',
 'October',
 'November',
 'December']

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

undertale_au = ["https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://undertale-au-fanon.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

regretevator = ["https://regretevator.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://regretevator.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://regretevator.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://regretevator.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://regretevator.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500"]

roblox = ["https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://roblox.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

vocaloid = ["https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://vocaloid.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

nights = ["https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://nights.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

msm = ["https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://mysingingmonsters.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

phighting = ["https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://phighting.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500"]

fortnite = ["https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://fortnite.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

animalcrossing = ["https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://animalcrossing.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

hazbinhotel = ["https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://hazbinhotel.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

uruseiyatsura = ["https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&limit=500&offset=","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231228065602&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231128052630&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20231018125513&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230919050858&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230808081127&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230627091113&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230613171215&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230602165331&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230429190940&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230330212318&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230314014930&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230220193258&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20230113040240&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221208211322&limit=500","https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221207114228&limit=500",
      "https://uruseiyatsura.fandom.com/wiki/Special:NewFiles?user=&mediatype%5B0%5D=BITMAP&mediatype%5B1%5D=ARCHIVE&start=&end=&wpFormIdentifier=specialnewimages&offset=20221129030150&limit=500"]

cr_games = ["ovenbreak", "kingdom", "tower"]

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
    global report 
    report = client.get_channel(1213349040050409512)
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    print('Bot is online!')
    await client.loop.create_task(check_time())

#Reputation giving and removing function
@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    try:
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
        except Forbidden:
            return
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
                #print(len(sourcelines)) #TEST
                source = ""
                for line in sourcelines:
                    source += f"{line} "
                try:
                    roll = {message.embeds[0].author.name.casefold():source.strip().casefold()}
                    #print(roll)
                    #print(source)
                    #print(str(list(roll.keys())[0])) #TEST
                    #Testing stuff
                    '''testvar = "reaper bird"
                    if str(list(roll.keys())[0]) == testvar:
                        await message.channel.send(f"{testvar} is loved by POOPMEISTER.-Q!")'''
                except AttributeError:
                    return
                try:
                    if "Belongs to" in str(message.embeds[0].footer.text):
                        return
                    #print(roll)
                    #print(source)
                    #print(str(list(roll.keys())[0])) #TEST
                    #Testing stuff
                    '''testvar = "reaper bird"
                    if str(list(roll.keys())[0]) == testvar:
                        await message.channel.send(f"{testvar} is loved by POOPMEISTER.-Q!")'''
                except AttributeError:
                    return
                for key, value in lovelist.items():
                    #print(key) #TEST
                    if int(key) == message.guild.id:
                        #print("Check 1 succeeded") #TEST
                        guildlovelist = lovelist[str(message.guild.id)]
                        for userlist in guildlovelist.items():
                            for entry in dict(userlist[1]).items():
                                #print(str(list(roll.keys())[0])) #TEST
                                if str(list(roll.keys())[0]) == entry[0]:
                                    if "Claim Rank" not in source:
                                        #print("Yes!") #TEST
                                        await message.channel.send(f"{entry[0]} is loved by <@{userlist[0]}>-Q!")
                for key, value in sourcelist.items():
                    if int(key) == message.guild.id:
                        #print("Test 1: passed.") #TEST
                        guildsourcelist = sourcelist[str(message.guild.id)]
                        for user, userlist in guildsourcelist.items():
                            #print(f"Checking {user} list...") #TEST
                            for usersource in userlist:
                                if str(usersource).strip().casefold() == source.strip().casefold():
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
                #await report.send(f"MSGlist is {msglist}")
                if len(msglist) > 100: #Index list should always be less than 100 just to make sure the little guy doesn't get too overwhelmed
                    for x in range(70):
                        msglist.pop(0) #Delete the oldest 70 messages from the list
                        #await report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                        #await report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                    msglist.append(message.content)
                    #print(msglist)
                else:
                    prevlength = len(msglist)
                    msglist.append(message.content)
                    #print(msglist)
                    #await report.send(f"MSGlist for {message.guild.name} updated-Q! Length has changed from {prevlength} to {len(msglist)}-Q!")
                stringlist[str(message.guild.id)] = msglist #Update the dictionary of indexed messages per server
            except KeyError:
                exceptionstring = format_exc()
                await report.send(f"{exceptionstring}\nIn {message.guild.name}")
                stringlist.update({str(message.guild.id): [message.content]}) #Adds a new entry to the dictionary if there's no indexed messages for the server
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {message.guild.name}")

#Check time every minute for reminder purposes
async def check_time():
    try:
        while True:
            now = datetime.now()
            flying_month = now.month
            flying_day = now.day
            flying_hour = now.hour
            flying_minute = now.minute
            flying_weekday = now.weekday()
            flying_datetime = [flying_month, flying_day, flying_hour, flying_minute, flying_weekday]
            for guild in guilds:
                try:
                    guild_reminders: dict = reminders[guild]
                except KeyError:
                    continue
                for user, reminder_list in guild_reminders.items():
                    user_reminders: dict = reminder_list
                    user_id = str(user)
                    for channel, channel_reminders in user_reminders.items():
                        for reason, date_time in channel_reminders.items():
                            if date_time == flying_datetime:
                                reminder_channel = await client.fetch_channel(int(channel))
                                await reminder_channel.send(f"<@{user_id}> reminding you about \"{reason}!\"")
            await asyncio.sleep(60)
    except Exception as e:
        exceptionstring = format_exc()
        current_guild: discord.Guild = client.fetch_guild(guild)
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {current_guild.name}")

#Mainly I just use this to make sure I'm running the latest version after I update him
@client.slash_command(description="Returns XyL-Q version number!", guild_ids=guilds)
async def version(ctx: discord.Interaction): 
    await ctx.respond(f"Hello-Q! I'm XyL-Q, running version {versionnum} released on {updatetime}-Q!\n\n__Changelog__\n{changes}")

#For me to refresh variables
@client.slash_command(description="Refresh all bot variables!", guild_ids=guilds)
async def refresh_vars(ctx: discord.Interaction): 
    if ctx.author.id in [120396380073099264, 1189313967831646278]:
        #Load individual user-to-user reputation database
        with open(f'{path}\\rep.json',"r+") as file:
            global rep
            try:
                text = json.loads(file.read())
                rep = text
            except JSONDecodeError as e:
                print(e)
                rep = {}
            file.close()

        #Load user total reputation database
        with open(f'{path}\\totalrep.json',"r+") as file:
            global totalrep
            try:
                text = json.loads(file.read())
                totalrep = text
            except JSONDecodeError as e:
                print(e)
                totalrep = {}
            file.close()

        #Load list of channels in which certain commands are disabled
        with open(f'{path}\\badid.json',"r+") as file:
            global badIDs
            try:
                text = json.loads(file.read())
                badIDs = text
            except JSONDecodeError as e:
                print(e)
                badIDs = {}
            file.close()

        #Load list of loved Mudae characters
        with open(f'{path}\\lovelist.json',"r+") as file:
            global lovelist
            try:
                text = json.loads(file.read())
                lovelist = text
            except JSONDecodeError as e:
                print(e)
                lovelist = {}
            file.close()

        #Load list of loved Mudae sources
        with open(f'{path}\\sourcelist.json',"r+") as file:
            global sourcelist
            try:
                text = json.loads(file.read())
                sourcelist = text
            except JSONDecodeError as e:
                print(e)
                sourcelist = {}
            file.close()


        #Load list of channels in which message caching is disabled
        with open(f'{path}\\badcache.txt',"r+") as file:
            global badcacheIDs
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
            global guilds
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
        await ctx.respond(f"Variables refreshed-Q!")
    else:
        await ctx.respond("Error-Q! You cannot use this command-Q!")

def check_img(img_link: str):
    #print(f"Checking {img_link}...") #TEST
    if img_link == "https://static.wikia.nocookie.net/carebears/images/8/80/Unlock_the_Magic_Here.jpg":
        #print(f"UTM here detected in {img_link}") #TEST
        return False
    elif img_link == "https://static.wikia.nocookie.net/carebears/images/1/16/Grumpy_Stub_fixed.jpg":
        #print(f"Grumpy stub detected in {img_link}") #TEST
        return False
    elif "data:image" in img_link:
        #print(f"data:image detected in {img_link}") #TEST
        return False
    else:
        return True

def ovenbreak_query(url: str, game):
    ovenbreak = {}
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    for td in soup.find_all('td'):
        for link in td.find_all('a'):
            cookie_name = link.get_text()
            if len(cookie_name) > 2:
                ovenbreak[cookie_name] = f"https://cookierun.fandom.com{link['href']}"
    return ovenbreak

def kingdom_query(url: str, game):
    kingdom = {}
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    for div in soup.select('div[class*="pi-theme"]'):
        for link in div.find_all('a'):
            cookie_name = link.get_text()
            if len(cookie_name) > 2:
                kingdom[cookie_name] = f"https://cookierunkingdom.fandom.com{link['href']}"
    return kingdom

def tower_query(url: str, game: str=None, cookies: dict=None):
    tower = {}
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for div in soup.select('div[class*="mw-body-content"]'):
        for li in div.find_all('li'):
            for link in li.find_all('a'):
                cookie_name = link.get_text()
                if (("Cookie" in cookie_name) and ("Cookies" not in cookie_name)) or ("GingerBrave" in cookie_name):
                    tower[cookie_name] = f"https://cookierun.fandom.com{link['href']}"
    return tower

#Command to get info on a certain Cookie Run cookie or choose a random one
@client.slash_command(description="Get information on a random Cookie Run cookie!", guild_ids=guilds)
async def cookie(ctx: discord.Interaction, game: discord.Option(str, choices=cr_games)=None): 
    try:
        await ctx.response.defer()
        ovenbreak_url = "https://cookierun.fandom.com/wiki/List_of_Cookies"
        kingdom_url = "https://cookierunkingdom.fandom.com/wiki/List_of_Cookies"
        tower_url = "https://cookierun.fandom.com/wiki/Cookie_Run:_Tower_of_Adventures#Cookies"
        witches_url = "https://cookierun.fandom.com/wiki/Cookie_Run:_Witch%27s_Castle#Cookies" #Don't want to use until they make pages for the new ones lol
        if game == "ovenbreak":
            cookies = ovenbreak_query(ovenbreak_url, game)
        if game == "kingdom":
            cookies = kingdom_query(kingdom_url, game)
        if game == "tower":
            cookies = tower_query(tower_url, game)
        if game == None:
            cookies = {}
            ovenbreak = ovenbreak_query(ovenbreak_url, game)
            kingdom = kingdom_query(kingdom_url, game)
            tower = tower_query(tower_url, game, cookies)
            for key, value in ovenbreak.items():
                cookies[key] = value
            for key, value in kingdom.items():
                if key in cookies.keys():
                    cookies[f"{key} (Kingdom)"] = value
                else:
                    cookies[key] = value
            for key, value in tower.items():
                if key in cookies.keys():
                    cookies[f"{key} (Tower of Adventures)"] = value
                else:
                    cookies[key] = value
            info = {}
            cookie_url = random.choice(list(cookies.values()))
        if game == None:
            if cookie_url in ovenbreak.values():
                cookie_game = "ovenbreak"
            elif cookie_url in kingdom.values():
                cookie_game = "kingdom"
            elif cookie_url in tower.values():
                cookie_game = "tower"
        print(cookie_game)
        cookie_url_chopped = str(cookie_url).split("/")
        cookie_gallery = f"{str(cookie_url)}/Gallery"
        cookie_name = cookie_url_chopped[-1].replace("_", " ")
        info['Name'] = cookie_name
        info['URL'] = cookie_url
        reqs = requests.get(cookie_url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        p = []
        prev_p = ""
        for link in soup.find_all('p'):
            if (f"<b>{cookie_name}</b>" in str(link)) or ((len(prev_p) > 0) and (len(p) == 1)):
                link_text = link.get_text()
                link_text = link_text.strip("\n").strip()
                prev_p = link_text
                p.append(link_text)
            if len(p) == 0:
                for link in soup.find_all('p'):
                    if (f"{cookie_name} (" in str(link)) or ((len(prev_p) > 0) and (len(p) == 1)):
                        link_text = link.get_text()
                        link_text = link_text.strip("\n").strip()
                        prev_p = link_text
                        p.append(link_text)
        description = ""
        for para in p:
            description += f"{para}\n"
        description = description.strip().replace("  ", " ")
        info['Description'] = description
        for link in soup.find_all('aside'):
            for div in link.select('div[data-source="pronouns"]'):
                for a in div.find_all('a'):
                    info['Pronouns'] = a.get_text()
            if (cookie_game == 'ovenbreak') or (cookie_game == 'tower'):
                for td in link.select('td[data-source="rarity"]'):
                    for img in td.find_all('img'):
                        info['Rarity'] = img['alt']
            if cookie_game == 'kingdom':
                for div in link.select('div[data-source="rarity"]'):
                    for img in div.find_all('img'):
                        info['Rarity'] = img['alt']
        backup_img = {}
        for link in soup.find_all('img'):
            try:
                if ((".jpg" in link["data-image-name"]) or (".png" in link["data-image-name"]) or (".webp" in link["data-image-name"]) and ("Cookie".casefold() in str(link["data-image-name"]).casefold())):
                        img_link = str(link["src"]).split("/revision")[0]
                        img_name = link["data-image-name"]
                        img_pass = check_img(img_link)
                        if img_pass == True:
                            backup_img[img_name] = img_link
            except KeyError:
                pass
        
        reqs = requests.get(cookie_gallery)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        img = {}

        for link in soup.find_all('img'):
            try:
                if ((".jpg" in link["data-image-key"]) or (".png" in link["data-image-key"]) or (".webp" in link["data-image-key"]) and ("Cookie".casefold() in str(link["data-image-key"]).casefold())):
                        img_link = str(link["src"]).split("/revision")[0]
                        img_name = link["data-image-key"]
                        img_pass = check_img(img_link)
                        if img_pass == True:
                            img[img_name] = img_link
                        
            except KeyError:
                pass
            try:
                cookie_img = random.choice(list(img.values()))
            except IndexError:
                    try:
                        cookie_img = random.choice(list(backup_img.values()))
                    except IndexError:
                        cookie_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png"
        else:
            try:
                embed = discord.Embed(title=info['Name'], description=info['Description'], url=info['URL'])
            except IndexError:
                ctx.respond("Index error occurred!")
            embed.set_image(url=cookie_img)
            try:
                embed.add_field(name="Pronouns", value=info["Pronouns"])
            except KeyError:
                embed.add_field(name="Pronouns", value="None")
            try:
                embed.add_field(name="Rarity", value=info["Rarity"])
            except KeyError:
                embed.add_field(name="Rarity", value="N/A")
            await ctx.respond(embed=embed)
            #await ctx.respond()
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Command to get info on a certain Care Bear or choose a random one
@client.slash_command(description="Get information on a random Care Bear, or a bear of your choice!", guild_ids=guilds)
async def care_bear(ctx: discord.Interaction, bear: str=None): 
    try:
        await ctx.response.defer()
        if bear == None:
            url = "https://carebears.fandom.com/wiki/Category:Care_Bears"
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            urls = []
            for link in soup.find_all('a'):
                url = link.get('href')
                if url != None:
                    if "/wiki/" in url: 
                        if url != "https://carebears.fandom.com/wiki/Care_Bears":
                            if "Bear" in url:
                                if "Category" not in url:
                                    if "User" not in url:
                                        urls.append(url)
            bear_url = f"https://carebears.fandom.com{random.choice(urls)}"
        else:
            url = f"https://carebears.fandom.com/wiki/Special:Search?query={bear}"
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            
            urls = []
            for link in soup.find_all('a'):
                try:
                    if link['data-position'] == '1':
                        urls.append(link)
                except KeyError:
                    pass
            try:    
                bear_url = urls[0]["href"]
            except IndexError:
                await ctx.respond(f"Bear {bear} not found!")
                return
        bear_url_chopped = str(bear_url).split("/")
        bear_gallery = f"{str(bear_url)}/Gallery"
        bear_name = bear_url_chopped[-1].replace("_", " ")
        #print(bear_name, bear_url) #TEST
        reqs = requests.get(bear_url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        p = []
        for link in soup.find_all('p'):
            if f"<b>{bear_name}</b>" in str(link):
                link_text = link.get_text()
                link_text = link_text.strip("\n")
                p.append(link_text)
        if len(p) == 0:
            for link in soup.find_all('p'):
                if f"{bear_name} is" in str(link):
                    link_text = link.get_text()
                    link_text = link_text.strip("\n")
                    p.append(link_text)
        aside_lists = []
        aside = []
        for link in soup.find_all('aside'):
            aside_lists.append(link.get_text().split("\n"))
        for aside_list in aside_lists:
            aside += aside_list
        info = {}
        try:
            info["Gender"] = aside[aside.index("Gender")+1]
        except ValueError:
            info["Gender"] = "None"

        try:
            info["Fur Colour"] = aside[aside.index("Fur Colour")+1]
        except ValueError:
            info["Fur Colour"] = "None"
        backup_img = {}
        for link in soup.find_all('img'):
            try:
                if (".jpg" in link["data-image-key"]) or (".png" in link["data-image-key"]) or (".webp" in link["data-image-key"]):
                        img_link = str(link["src"]).split("/revision")[0]
                        img_name = link["data-image-key"]
                        img_pass = check_img(img_link)
                        if img_pass == True:
                            backup_img[img_name] = img_link
            except KeyError:
                pass
        
        reqs = requests.get(bear_gallery)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        img = {}

        for link in soup.find_all('img'):
            try:
                if (".jpg" in link["data-image-key"]) or (".png" in link["data-image-key"]) or (".webp" in link["data-image-key"]):
                        img_link = str(link["data-src"]).split("/revision")[0]
                        img_name = link["data-image-key"]
                        img_pass = check_img(img_link)
                        if img_pass == True:
                            img[img_name] = img_link
            except KeyError:
                pass
        try:
            bear_img = random.choice(list(img.values()))
        except IndexError:
                try:
                    bear_img = random.choice(list(backup_img.values()))
                except IndexError:
                    bear_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png"
        #print(bear_img) #TEST
        if "Bear" not in bear_name:
            await ctx.respond(f"Bear {bear} not found!")
        else:
            try:
                embed = discord.Embed(title=bear_name, description=p[0].split("\n")[-1], url=bear_url)
            except IndexError:
                embed = discord.Embed(title=bear_name, description=p, url=bear_url)
            embed.set_image(url=bear_img)
            embed.add_field(name="Gender", value=info["Gender"])
            embed.add_field(name="Fur color", value=info["Fur Colour"])
            await ctx.respond(embed=embed)
            #await ctx.respond()
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Simple way for users to check reputation, also revised by ChatGPT even though I didn't ask it to revise this either
@client.slash_command(description="Shows you your reputation and other related stats!")
async def reputation(ctx: discord.Interaction, user: str=None):
    try:
        guild_id_str = str(ctx.guild.id)
        if user == None:
            user_id_str = str(ctx.author.id)
            member: discord.User = ctx.author
        else:
            user_id_str = user.strip("<>@")
            guild: discord.Guild = ctx.guild
            try:
                member: discord.User = await guild.fetch_member(int(user_id_str))
            except ValueError:
                await ctx.respond("Error-Q! Please input the user by @-ing them-Q!")

        embed = discord.Embed(title=f"{member.display_name}'s reputation stats-Q!",
                            color=member.color)
        embed.set_thumbnail(url=member.display_avatar.url)

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
        repreceivedusers = {}
        for giver_id, given_to in guild_rep.items():
            if user_id_str in given_to:
                repreceivedusers[giver_id] = given_to[user_id_str]
        if len(repreceivedusers) > 0:
            sorted_given_rep = sorted(repreceivedusers.items(), key=lambda x: x[1], reverse=True)
            for giver_id, amount in sorted_given_rep[:3]:
                received_rep_str += f"<@{giver_id}>: {amount} rep\n"
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

#Set reminder for user
@client.slash_command(description="Sets a reminder based on user input!", guild_ids=guilds)
async def set_reminder(ctx: discord.Interaction, timezone: discord.Option(str, choices=common_timezones), time: str, month: discord.Option(str, choices=months)=datetime.now().month, day: int=datetime.now().day, year:int=datetime.now().year, reason: str=None): 
    try:
        global reminders
        user = str(ctx.user.id)
        guild = str(ctx.guild.id)
        try:
            guild_reminders = reminders[guild]
        except KeyError:
            reminders[guild] = {}
            guild_reminders = {}
        try:
            user_reminders = guild_reminders[user]
        except KeyError:
            guild_reminders[user] = {}
            user_reminders = {}
        channel = str(ctx.channel.id)
        try:
            channel_reminders = user_reminders[channel]
        except KeyError:
            user_reminders[channel] = {}
            channel_reminders = {}
        if any(elem in time.casefold() for elem in ["am", "pm"]):
            timesplitters = time.split(":")
            if any(elem in timesplitters[1].casefold() for elem in ["am", "pm"]):
                am_or_pm = timesplitters[1][-2:].strip()
                print(am_or_pm)
                timesplitters[1] = timesplitters[1][:-2]
                if am_or_pm.casefold() == "am":
                    hour = int(timesplitters[0])
                elif am_or_pm.casefold() == "pm":
                    hour = int(timesplitters[0])
                    if hour < 12:
                        hour = hour + 12
                    elif hour == 12:
                        hour = 12
                    else:
                       await ctx.respond("Error: Invalid hour given-Q! Accepted hours are 0-23!") 
                else:
                    await ctx.respond("Error: Invalid time entry-Q! Examples of accepted formats are: '16:50', '4:50PM', or '4:50 PM'-Q!")
                    return
                minute = timesplitters[1]
            else:
                timesplitters.append(timesplitters[1].split(" "))
        else:
            timesplitters = time.split(":")
            try:
                hour = int(timesplitters[0])
                minute = timesplitters[1]
            except ValueError:
                ctx.respond("Error: Invalid time entry-Q! Examples of accepted formats are: '16:50', '4:50PM', or '4:50 PM'-Q!")
                return
        now = datetime.now()
        if type(month) == str:
            num_month = months.index(month)+1
            word_month = month
        else:
            num_month = month
            word_month = months[num_month-1]
        date_time = datetime(year=int(year), month=num_month, day=int(day), hour=int(hour), minute=int(minute))
        timezone: pytz.tzinfo.DstTzInfo = pytz.timezone(timezone)
        localized: datetime = timezone.localize(date_time)
        output = [localized.month, localized.day, localized.hour, localized.minute, localized.weekday()]
        if reason != None:
            channel_reminders[reason] = output
            user_reminders[channel] = channel_reminders
            guild_reminders[user] = user_reminders
            reminders[guild] = guild_reminders
            await ctx.respond(f"Got it-Q! I've set a reminder for '{reason}' at {time} on {month} {day}, {year}!")
        else:
            key = f"{now.year} {now.month} {now.day} {now.hour} {now.minute} {now.second}"
            channel_reminders[key] = output
            user_reminders[channel] = channel_reminders
            guild_reminders[user] = user_reminders
            reminders[guild] = guild_reminders
            await ctx.respond(f"Got it-Q! I've set a reminder at {hour}:{minute} on {word_month} {day}, {year}!")
        with open(f'{path}\\reminders.json', "w") as file:
            json.dump(reminders, file)
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
            await report.send(f"{exceptionstring}\nIn {ctx.guild.name}")
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
            guildlovelist = lovelist[str(ctx.guild.id)]
        except KeyError:
            guildlovelist = {}
        try:
            userlovelist = guildlovelist[IDstring]
        except KeyError:
            userlovelist = {}
        userlovelist[character.casefold().strip()] = source.casefold().strip()
        guildlovelist[IDstring] = userlovelist
        lovelist[str(ctx.guild.id)] = guildlovelist
        with open(f'{path}\\lovelist.json', "w") as file:
            json.dump(lovelist, file)
        if user != None:
            guild: discord.Guild = ctx.guild
            member: discord.User = await guild.fetch_member(int(IDstring))
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {character} from {source} to {member.display_name}'s lovelist-Q!")
        else:
            await ctx.respond(f"{random.choice(aff)}-Q! I've added {character} from {source} to your lovelist-Q!")
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
            guildsourcelist = sourcelist[str(ctx.guild.id)]
        except KeyError:
            guildsourcelist = {}
        try:
            usersourcelist = guildsourcelist[IDstring]
        except KeyError:
            usersourcelist = []
        usersourcelist.append(source.casefold().strip())
        guildsourcelist[IDstring] = usersourcelist
        sourcelist[str(ctx.guild.id)] = guildsourcelist
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
      
class prev_next(discord.ui.View):
    def __init__(self, content, pages, member: discord.User):
        super().__init__()
        self.value = None
        self.page = 1
        self.content = content
        self.pages = pages
        self.member = member
    
    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji="◀️")
    async def prev(self, button, interaction: discord.Interaction):
        if self.page > 1:
            self.page -= 1
        else:
            self.page = self.pages
        embed = discord.Embed(title="",
                            color=self.member.color)
        embed.set_author(name=f"{self.member.display_name}'s lovelist-Q!", icon_url=self.member.display_avatar.url)
        embed.add_field(name="", value=self.content[self.page - 1])
        embed.set_footer(text=f"Page {self.page} / {self.pages}")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji="▶️")
    async def next(self, button, interaction: discord.Interaction):
        if self.page < self.pages:
            self.page += 1
        else:
            self.page = 1
        embed = discord.Embed(title="",
                            color=self.member.color)
        embed.set_author(name=f"{self.member.display_name}'s lovelist-Q!", icon_url=self.member.display_avatar.url)
        embed.add_field(name="", value=self.content[self.page - 1])
        embed.set_footer(text=f"Page {self.page} / {self.pages}")
        await interaction.response.edit_message(embed=embed)


#Lets you check your list of loved characters
@client.slash_command(description="Shows your list of loved characters!", guild_ids=guilds)
async def view_lovelist(ctx: discord.Interaction, list_to_view: discord.Option(str, choices=["characters", "sources"]), user: str=None):
    try:
        if user == None:
            IDstring = str(ctx.author.id)
            member: discord.User = ctx.author
        else:
            IDstring = user.strip("<>@")
            guild: discord.Guild = ctx.guild
            member: discord.User = await guild.fetch_member(int(IDstring))
        if list_to_view == "characters":
            try:
                guildlovelist = lovelist[str(ctx.guild.id)]
            except KeyError:
                guildlovelist = {}
                await ctx.send("Your characters lovelist is empty-Q!")
                return
            try:
                userlovelist: dict = guildlovelist[IDstring]
            except KeyError:
                if IDstring == str(ctx.author.id):
                    await ctx.send("Your characters lovelist is empty-Q!")
                    userlovelist: dict = {}
                    return
                else:
                    await ctx.send(f"{member.display_name}'s characters lovelist is empty-Q!")
            if len(userlovelist) > 0:
                per_page = 15
                content = []
                pages = (len(userlovelist) + per_page - 1) // per_page
                user_loved = list(userlovelist.items())
                current_page = 1
                for page in range(pages):
                    start_index = page * per_page
                    end_index = start_index + per_page
                    page_items = user_loved[start_index:end_index]
                    page_content = ""
                    for num, (key, value) in enumerate(page_items, start=1):
                        line = f"{num + start_index}. **{key}** | {value}" 
                        page_content += f"{line}\n"
                    content.append(page_content)
                embed = discord.Embed(title="",
                                color=member.color)
                embed.set_author(name=f"{member.display_name}'s characters lovelist-Q!", icon_url=member.display_avatar.url)
                embed.add_field(name="", value=content[current_page - 1])
                embed.set_footer(text=f"Page {current_page} / {pages}")
                interaction: discord.Interaction = await ctx.respond(embed=embed, view=prev_next(content, pages, member))
                message: discord.Message = interaction.message
        elif list_to_view == "sources":
            try:
                guildlovelist = sourcelist[str(ctx.guild.id)]
            except KeyError:
                guildlovelist = {}
                await ctx.send("Your sources lovelist is empty-Q!")
                return
            try:
                userlovelist: list = guildlovelist[IDstring]
            except KeyError:
                if IDstring == str(ctx.author.id):
                    await ctx.send("Your sources lovelist is empty-Q!")
                    userlovelist = []
                    return
                else:
                    await ctx.send(f"{member.display_name}'s sources lovelist is empty-Q!")
            if len(userlovelist) > 0:
                per_page = 15
                content = []
                pages = (len(userlovelist) + per_page - 1) // per_page
                user_loved = list(userlovelist)
                current_page = 1
                for page in range(pages):
                    start_index = page * per_page
                    end_index = start_index + per_page
                    page_items = user_loved[start_index:end_index]
                    page_content = ""
                    for num, source in enumerate(page_items, start=1):
                        line = f"{num + start_index}. **{source}**" 
                        page_content += f"{line}\n"
                    content.append(page_content)
                embed = discord.Embed(title="",
                                color=member.color)
                embed.set_author(name=f"{member.display_name}'s sources lovelist-Q!", icon_url=member.display_avatar.url)
                embed.add_field(name="", value=content[current_page - 1])
                embed.set_footer(text=f"Page {current_page} / {pages}")
                interaction: discord.Interaction = await ctx.respond(embed=embed, view=prev_next(content, pages, member))
                message: discord.Message = interaction.message
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

def get_image(url_list: str, base_url: str):
    print("-"*50)
    url = random.choice(url_list)
    
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    urls = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url != None:
            if (".png" in url) or (".jpg" in url):
                if "File:" in url:
                    urls.append(url)
    page = f"{base_url}{random.choice(urls)}"
    reqsagain = requests.get(page)
    soup = BeautifulSoup(reqsagain.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url != None:
            if (".png" in url) or (".jpg" in url):
                    if "images" in url:
                        print("images", url)
                        urls.append(url)
        if not urls:  # If no images are found, restart the loop
            continue
    try:
        if url_list == mcwiki:
            image_link = f"{base_url}{random.choice(urls)}"  
        else:
            image_url = random.choice(urls)
            print(image_url[0:8])
            if image_url[0:8] != "https://":
                image_link = f"{base_url}{image_url}" 
            else:
                image_link = image_url
    except IndexError:
        image_link = random.choice(backup_img)
    return image_link

#MY MAGNUM OPUS (the meme command)
@client.slash_command(description="Makes a meme based on parameters given!", guild_ids=guilds)
async def meme(ctx: discord.Interaction, top_text: str=None, bottom_text: str=None, image_link: str=None, image_upload: discord.Attachment=None, wiki: discord.Option(str, choices=wikis)=None): 
    try:
        await ctx.response.defer()
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
                await report.send(f"{exceptionstring}\nIn {ctx.guild.name}")
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
                        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")
                        image_link = "https://mario.wiki.gallery/images/f/fe/36-Diddy_Kong.png"
                    
                #elif numba < 1:
                    #This list is empty right now so once I populate that list I'll add this back in
                    #image_link = random.choice(imglist)
                else:   
                    if wiki == None:
                        wiki = random.choice(wikis)     
                    if wiki == "Mario":
                        image_link = get_image(mariowiki, "https://www.mariowiki.com")
                    if wiki == "Minecraft":
                        image_link = get_image(mcwiki, "https://minecraft.wiki")
                    if wiki == "Super Smash Bros.":
                        image_link = get_image(ssb, "https://supersmashbros.fandom.com")
                    if wiki == "cb":
                        image_link = get_image(cb, "https://carebears.fandom.com")
                    if wiki == "Cookie Run":
                        image_link = get_image(cr, "https://cookierun.fandom.com")
                        '''cookie = random.choice(["cr", "crk"])
                        if cookie == "cr":
                            image_link = get_image(cr, "https://cookierun.fandom.com")
                        if cookie == "crk":
                            image_link = get_image(crk, "https://cookierunkingdom.fandom.com")'''
                    if wiki == "Regretevator":
                        image_link = get_image(regretevator, "https://regretevator.fandom.com")
                    if wiki == "Undertale AUs":
                        image_link = get_image(undertale_au, "https://undertale-au-fanon.fandom.com")
                    if wiki == "Roblox":
                        image_link = get_image(roblox, "https://roblox.fandom.com")
                    if wiki == "Vocaloid":
                        image_link = get_image(vocaloid, "https://vocaloid.fandom.com")
                    if wiki == "NiGHTS":
                        image_link = get_image(nights, "https://nights.fandom.com")
                    if wiki == "My Singing Monsters":
                        image_link = get_image(msm, "https://mysingingmonsters.fandom.com")
                    if wiki == "PHIGHTING!":
                        image_link = get_image(phighting, "https://phighting.fandom.com")
                    if wiki == "Fortnite":
                        image_link = get_image(fortnite, "https://fortnite.fandom.com")
                    if wiki == "Animal Crossing":
                        image_link = get_image(animalcrossing, "https://animalcrossing.fandom.com")
                    if wiki == "Hazbin Hotel":
                        image_link = get_image(hazbinhotel, "https://hazbinhotel.fandom.com")
                    if wiki == "Urusei Yatsura":
                        image_link = get_image(uruseiyatsura, "https://uruseiyatsura.fandom.com")
        memelink = f"https://api.memegen.link/images/custom/{top_text_new}/{bottom_text_new}.png?background={image_link}"
        await ctx.followup.send(content=memelink)
    except Exception as e:
        exceptionstring = format_exc()
        await ctx.respond("An error has occurred! Please try again!")
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

client.run(TOKEN)