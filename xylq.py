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
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import re

status = "Creatures of Sonaria"
#status = "Testing new features!"
versionnum = "8.2"
updatetime = "2025/05/25 13:26"
changes = "**(8.2)** Made it so that medal and tomato reacts are picked up regardless of the message age (FINALLY!!!!)"
path = os.getcwd()
print(f"XyL-Q v{versionnum}")
print(updatetime)
print("womp womp")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TOKEN = os.getenv('TEST_TOKEN')
intents=discord.Intents.all()
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

#Load list of loved Mudae characters
with open(f'{path}\\quotes.json',"r+") as file:
    try:
        text = json.loads(file.read())
        quotes = text
    except JSONDecodeError as e:
        print(e)
        quotes = {}
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

cr_games = ["ovenbreak", "kingdom", "tower"]

stringlist = {} #I don't remember what this even is
aff = ["Okay", "Alright", "Got it", "Affirmative","Sounds good", "No problem", "Done"] #Different affirmative phrases the bot can say when asked to do something
selfrep = ["You're giving reputation to me-Q?? Well, thank you-Q! ^^","Oh...thank you so much for the reputation-Q! I will take good care of it-Q! ^^"] #Cutie little guy messages for when reputation is awarded to XyL-Q
bots = [429305856241172480, 439205512425504771, 247283454440374274, 431544605209788416] #Bot IDs so XyL-Q can avoid indexing their messages
imglist = [] #Instantiating list for later

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
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    try:
        try:
            if str(payload.emoji) == "🏅": #Might add all the other medal emojis too just for funsies
                #Heavily revised by ChatGPT which was not necessarily what I even wanted it to do
                guild_id_str = str(payload.guild_id)
                user_id_str = str(payload.user_id)
                reaction_message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
                author_id_str = str(reaction_message.author.id)

                # Check for self-reputation or specific user ID conditions
                if reaction_message.author == client.user:
                    await reaction_message.channel.send(random.choice(selfrep))
                elif author_id_str == "1204234942897324074":
                    await reaction_message.channel.send("My apologies, but I cannot handle giving reputation to tuppers-Q!")
                    return  # Exit for specific user conditions
                elif user_id_str == author_id_str:
                    await reaction_message.channel.send("My apologies, but I cannot let you give reputation to yourself-Q!")
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
            

                await reaction_message.channel.send(f"<@{user_id_str}> has given <@{author_id_str}> +1 reputation-Q!")

                # Write to files
                with open(f'{path}\\rep.json', "w") as file:
                    json.dump(rep, file)
                
                with open(f'{path}\\totalrep.json', "w") as file:
                    json.dump(totalrep, file)
            if str(payload.emoji) == "🍅":
                guild_id_str = str(payload.guild_id)
                user_id_str = str(payload.user_id)
                reaction_message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
                author_id_str = str(reaction_message.author.id)

                if reaction_message.author == client.user:
                    await reaction_message.channel.send("I will not permit uncleanliness on my person-Q!!")
                    return

                # Check for self-reputation or specific user ID conditions
                if reaction_message.author == client.user:
                    await reaction_message.channel.send(random.choice(selfrep))
                elif author_id_str == "1204234942897324074":
                    await reaction_message.channel.send("My apologies, but I cannot handle taking reputation from tuppers-Q!")
                    return  # Exit for specific user conditions
                elif user_id_str == author_id_str:
                    await reaction_message.channel.send("Why would you want to take away your own rep-Q?!")
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
                    await reaction_message.channel.send("This user has no rep to take away-Q!")
                if totalrep[guild_id_str][author_id_str] <= 0:
                    totalrep[guild_id_str][author_id_str] = 0
                    await reaction_message.channel.send("This user has no rep to take away-Q!")
                else:
                    # Update totalrep
                    totalrep[guild_id_str][author_id_str] -= 1
                    await report.send(f"Total reputation of {author_id_str} updated. It is now {totalrep[guild_id_str][author_id_str]}")

                    await reaction_message.channel.send(f"<@{user_id_str}> threw a tomato at <@{author_id_str}>-Q! Rather unclean of you-Q…")
        except Forbidden:
            return
        # Write to reputation databases
        with open(f'{path}\\rep.json', "w") as file:
            json.dump(rep, file)
        
        with open(f'{path}\\totalrep.json', "w") as file:
            json.dump(totalrep, file)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {reaction_message.guild.name}")

@client.event
async def on_message(message: discord.Message):
    try:
        if ((f"<@{client.user.id}>") in message.content): 
                if (message.reference):
                    new_quote = message.reference.resolved.content
                    quote_author = message.reference.resolved.author.id
                    quote_server = message.guild.id
                elif re.search(r"https:\/\/discord\.com\/channels\/(@me|\d+)\/\d+\/\d+", message.content):
                    msgurl = (re.search(r"https:\/\/discord\.com\/channels\/(@me|\d+)\/\d+\/\d+", message.content)).group()
                    params = msgurl.split("/")[4:7]
                    if params[0] == "@me":
                        await message.reply(f"Error-Q! Cannot add direct messages to quote list-Q!")
                        return
                    else:
                        guild = await client.fetch_guild(int(params[0]))
                        channel = await client.fetch_channel(int(params[1]))
                        quote_message = await channel.fetch_message(int(params[2]))
                        new_quote = quote_message.content
                        quote_author = quote_message.author.id
                        quote_server = guild.id
                try:
                    quote_dict = quotes[str(quote_server)]
                except KeyError:
                    quote_dict = {}
                try:
                    author_list = quote_dict[str(quote_author)]
                except KeyError:
                    author_list = []
                author_list.append(new_quote)
                quote_dict[str(quote_author)] = author_list
                quotes[str(quote_server)] = quote_dict
                with open(f'{path}\\quotes.json',"w") as file:
                    myJson = json.dumps(quotes)
                    file.write(myJson)
                    file.close()
                await message.reply(f"{random.choice(aff)}-Q! Quote added-Q!")
        try:
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
        except AttributeError:
            return
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
@client.slash_command(description="Returns XyL-Q version number!")
async def version(ctx: discord.Interaction): 
    await ctx.respond(f"Hello-Q! I'm XyL-Q, running version {versionnum} released on {updatetime}-Q!\n\n__Changelog__\n{changes}")

#For me to refresh variables
@client.slash_command(description="Refresh all bot variables!")
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
@client.slash_command(description="Get information on a random Cookie Run cookie!")
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
@client.slash_command(description="Get information on a random Care Bear, or a bear of your choice!")
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
        given_rep_str = given_rep_str or "Nobody-Q! Perhaps you should pay more attention to your fellow citizens-Q? Or perhaps they just aren’t humorous enough-Q..."
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
        received_rep_str = received_rep_str or "Nobody-Q! But I’m sure we have some in our reserves on Xylitol Planet for you-Q!"
        embed.add_field(name="You've received the most rep from:", value=received_rep_str, inline=False)

        await ctx.respond(embed=embed)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Set reminder for user
@client.slash_command(description="Sets a reminder based on user input!")
async def set_reminder(ctx: discord.Interaction, timezone: discord.Option(str, choices=common_timezones), time: str, month: discord.Option(str, choices=months)=None, day: int=None, year:int=None, reason: str=None): 
    try:
        global reminders
        user = str(ctx.user.id)
        guild = str(ctx.guild.id)
        if month == None:
            month = datetime.now().month
        if day == None:
            day = datetime.now().day
        if year == None:
            year = datetime.now().year
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
                       await ctx.respond("Error: Invalid hour given-Q! Accepted hours are 0 through 23-Q!") 
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
            await ctx.respond(f"Got it-Q! I've set a reminder for '{reason}' at {time} on {word_month} {day}, {year}-Q!")
        else:
            key = f"{now.year} {now.month} {now.day} {now.hour} {now.minute} {now.second}"
            channel_reminders[key] = output
            user_reminders[channel] = channel_reminders
            guild_reminders[user] = user_reminders
            reminders[guild] = guild_reminders
            await ctx.respond(f"Got it-Q! I've set a reminder at {hour}:{minute} on {word_month} {day}, {year}-Q!")
        with open(f'{path}\\reminders.json', "w") as file:
            json.dump(reminders, file)
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Disables a command's use in a certain channel, not really even sure what the use case for this is
@client.slash_command(description="Disables a command in a given channel!")
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

def get_user_characters(user: str):
    user_charas: dict = {}
    try:
        for guild in lovelist.keys():
            try:
                if lovelist[guild][user]:
                    for key, value in dict(lovelist[guild][user]).items():
                        user_charas[key] = value
            except KeyError:
                continue
    except Exception as e:
        exceptionstring = format_exc()
        print(exceptionstring)
    return user_charas

def get_user_sources(ctx: discord.AutocompleteContext):
    global user_sources
    user_sources = []
    user = str(ctx.interaction.user.id)
    try:
        for guild in sourcelist.keys():
            try:
                if sourcelist[guild][user]:
                    user_sources += sourcelist[guild][user]
            except KeyError:
                continue
        keys = user_sources
    except Exception as e:
        exceptionstring = format_exc()
        print(exceptionstring)
    return keys

#Utility for Mudae rolls, notifies a user of any character given with this command
@client.slash_command(description="Loves a character from Mudae to notify you later if that character is rolled!")
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
@client.slash_command(description="Loves a source from Mudae to notify you later if any character from that source is rolled!")
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
      
class lovelist_prev_next(discord.ui.View):
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
@client.slash_command(description="Shows your list of loved characters!")
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
                await ctx.respond("Your characters lovelist is empty-Q!")
                return
            try:
                userlovelist: dict = guildlovelist[IDstring]
            except KeyError:
                if IDstring == str(ctx.author.id):
                    await ctx.respond("Your characters lovelist is empty-Q!")
                    userlovelist: dict = {}
                    return
                else:
                    await ctx.respond(f"{member.display_name}'s characters lovelist is empty-Q!")
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
                interaction: discord.Interaction = await ctx.respond(embed=embed, view=lovelist_prev_next(content, pages, member))
                message: discord.Message = interaction.message
        elif list_to_view == "sources":
            try:
                guildlovelist = sourcelist[str(ctx.guild.id)]
            except KeyError:
                guildlovelist = {}
                await ctx.respond("Your sources lovelist is empty-Q!")
                return
            try:
                userlovelist: list = guildlovelist[IDstring]
            except KeyError:
                if IDstring == str(ctx.author.id):
                    await ctx.respond("Your sources lovelist is empty-Q!")
                    userlovelist = []
                    return
                else:
                    await ctx.respond(f"{member.display_name}'s sources lovelist is empty-Q!")
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
                interaction: discord.Interaction = await ctx.respond(embed=embed, view=lovelist_prev_next(content, pages, member))
                message: discord.Message = interaction.message
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

def get_user_lovelists(ctx: discord.AutocompleteContext):
    global user_servers
    user_servers = {}
    user = str(ctx.interaction.user.id)
    try:
        for guild in lovelist.keys():
            server = client.get_guild(int(guild))
            try:
                if lovelist[guild][user]:
                    user_servers[server.name] = guild
            except KeyError:
                continue
        keys = list(user_servers.keys())
        if ctx.interaction.guild.name in keys:
            keys.pop(keys.index(ctx.interaction.guild.name))
    except Exception as e:
        exceptionstring = format_exc()
        print(exceptionstring)
    return keys

def get_user_sourcelists(ctx: discord.AutocompleteContext):
    global user_servers
    user_servers = {}
    user = str(ctx.interaction.user.id)
    try:
        for guild in sourcelist.keys():
            server = client.get_guild(int(guild))
            try:
                if sourcelist[guild][user]:
                    user_servers[server.name] = guild
            except KeyError:
                continue
        keys = list(user_servers.keys())
        if ctx.interaction.guild.name in keys:
            keys.pop(keys.index(ctx.interaction.guild.name))
    except Exception as e:
        exceptionstring = format_exc()
        print(exceptionstring)
    return keys

#Lets you import your loved characters from another server
@client.slash_command(description="Imports your loved character from another server!")
async def import_lovelist(ctx: discord.Interaction, server: discord.Option(str, "Select an item", autocomplete=get_user_lovelists)):
    try:
        server_id = str(user_servers[server])
        cur_server_id = str(ctx.guild.id)
        user_id = str(ctx.user.id)
        imported_list = lovelist[server_id][user_id]
        try:
            serverlist = lovelist[cur_server_id]
        except KeyError:
            serverlist = []
        try:
            cur_user_list = serverlist[user_id]
        except KeyError:
            cur_user_list = []
        for key, value in imported_list.items():
            cur_user_list[key] = value
        lovelist[server_id][user_id] = cur_user_list
        await ctx.respond(f"Done-Q! Your lovelist from {server} has been imported-Q!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

@client.slash_command(description="Imports your loved sources from another server!")
async def chara_chooser(ctx: discord.Interaction):
    try:
        characters = get_user_characters(str(ctx.user.id))
        if len(characters.keys()) > 1: 
            character_one = random.choice(list(characters.keys()))
            character_two = random.choice(list(characters.keys()))
            if character_one == character_two:
                character_two = random.choice(list(characters.keys()))
        else:
            await ctx.respond(f"Error: Character list too short! Add more characters using /love_character!")
        await ctx.respond(f"Your two characters are **{character_one}** from {characters[character_one]} and **{character_two}** from {characters[character_two]}!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

@client.slash_command(description="Imports your loved sources from another server!")
async def import_sourcelist(ctx: discord.Interaction, server: discord.Option(str, "Select an item", autocomplete=get_user_sourcelists)):
    try:
        server_id = str(user_servers[server])
        cur_server_id = str(ctx.guild.id)
        user_id = str(ctx.user.id)
        imported_list = sourcelist[server_id][user_id]
        try:
            cur_user_list = sourcelist[cur_server_id][user_id]
        except KeyError:
            cur_user_list = []
        cur_user_list += imported_list
        try:
            sourcelist[cur_server_id][user_id] = list(set(cur_user_list))
        except KeyError:
            sourcelist[cur_server_id] = {}
            sourcelist[cur_server_id][user_id] = list(set(cur_user_list))
        await ctx.respond(f"Done-Q! Your sourcelist from {server} has been imported-Q!")
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

def ud_format(string: str):
    brackets = re.findall(r"\[(.*?)\]", string)
    replacements = []
    for term in brackets:
        linkterm = str(term).replace(" ", "%20")
        replacements.append(f"[{term}](https://www.urbandictionary.com/define.php?term={linkterm})")
    replacer = iter(replacements)
    newdef = re.sub(r"\[(.*?)\]", lambda match: next(replacer), string)

    return newdef

class urban_prev_next(discord.ui.View):
    def __init__(self, definitions: list):
        super().__init__()
        self.value = None
        self.page = 1
        self.pages = len(definitions)
        self.definitions = definitions
    
    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji="◀️")
    async def prev(self, button, interaction: discord.Interaction):
        if self.page > 1:
            self.page -= 1
        else:
            self.page = self.pages
        index = self.page - 1
        definition = ud_format(str(self.definitions[index]["definition"]))
        example = ud_format(str(self.definitions[index]["example"]))
        title = str(self.definitions[index]["word"])
        if len(definition) > 1000:
            definition = definition[0:1000].strip() + "..."
        if len(example) > 1000:
            example = example[0:1000].strip() + "..."
        link = str(self.definitions[index]["permalink"])
        date = datetime.strptime(str(self.definitions[index]["written_on"]), "%Y-%m-%dT%H:%M:%S.%fZ")
        author = str(self.definitions[index]["author"])
        embed = discord.Embed(title=title, timestamp=date, url=link)
        embed.set_author(name=author)
        embed.add_field(name="Definition", value=definition)
        embed.add_field(name="Example", value=f"{example}")
        embed.set_footer(text=f"Page {self.page} / {self.pages}")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(style=discord.ButtonStyle.secondary , emoji="▶️")
    async def next(self, button, interaction: discord.Interaction):
        if self.page < self.pages:
            self.page += 1
        else:
            self.page = 1
        index = self.page - 1
        definition = ud_format(str(self.definitions[index]["definition"]))
        example = ud_format(str(self.definitions[index]["example"]))
        title = str(self.definitions[index]["word"])
        if len(definition) > 1000:
            definition = definition[0:1000].strip() + "..."
        if len(example) > 1000:
            example = example[0:1000].strip() + "..."
        link = str(self.definitions[index]["permalink"])
        date = datetime.strptime(str(self.definitions[index]["written_on"]), "%Y-%m-%dT%H:%M:%S.%fZ")
        author = str(self.definitions[index]["author"])
        embed = discord.Embed(title=title, timestamp=date, url=link)
        embed.set_author(name=author)
        embed.add_field(name="Definition", value=definition)
        embed.add_field(name="Example", value=f"{example}")
        embed.set_footer(text=f"Page {self.page} / {self.pages}")
        await interaction.response.edit_message(embed=embed)

#Quote command
@client.slash_command(description="Choose a random quote from this server!")
async def quote(ctx: discord.Interaction, user: str=None):
    try:
        if user == None:
            try:
                quote_dict = dict(quotes[str(ctx.guild.id)])
                quote_pool = []
                for key, value in quote_dict.items():
                    for quote in value:
                        try:
                            member: discord.User = await ctx.guild.fetch_member(int(key))
                            quote_pool.append(f"**{member.display_name}:** {quote}")
                        except discord.errors.NotFound:
                            quote_pool.append(f"**Deleted User:** {quote}")
                quote_chosen = random.choice(quote_pool)
                await ctx.respond(quote_chosen)
            except KeyError:
                await ctx.respond("Error-Q! No quotes found for this server-Q!\n-# Sorry-Q...")
                return
        else:
            try:
                quote_dict = dict(quotes[str(ctx.guild.id)])
                user_id_str = user.strip("<>@")
                guild: discord.Guild = ctx.guild
                try:
                    member: discord.User = await guild.fetch_member(int(user_id_str))
                except ValueError:
                    await ctx.respond("Error-Q! Please input the user by @-ing them-Q!")
                    return
                author_list = quote_dict[str(user_id_str)]
                quote_chosen = random.choice(author_list)
                await ctx.respond(f"**{member.display_name}:** {quote_chosen}")
            except KeyError:
                await ctx.respond("Error-Q! No quotes found for this user-Q!\n-# Apologies-Q...")
                return
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

#Search Urban Dictionary for word definition
@client.slash_command(description="Searches the definition of a term in Urban Dictionary!")
async def urban_dictionary(ctx: discord.Interaction, term: str):
    try:
        response = requests.get(f"https://api.urbandictionary.com/v0/define?term={term}").json()
        definitions = list(response["list"])
        definition = ud_format(str(definitions[0]["definition"]))
        example = ud_format(str(definitions[0]["example"]))
        title = str(definitions[0]["word"])
        if len(definition) > 1000:
            definition = definition[0:1000].strip() + "..."
        if len(example) > 1000:
            example = example[0:1000].strip() + "..."
        link = str(definitions[0]["permalink"])
        date = datetime.strptime(str(definitions[0]["written_on"]), "%Y-%m-%dT%H:%M:%S.%fZ")
        author = str(definitions[0]["author"])
        embed = discord.Embed(title=title, timestamp=date, url=link)
        embed.set_author(name=author)
        embed.add_field(name="Definition", value=definition)
        embed.add_field(name="Example", value=f"{example}")
        embed.set_footer(text=f"Page 1 / {len(definitions)}")
        interaction: discord.Interaction = await ctx.respond(embed=embed, view=urban_prev_next(definitions))
        message: discord.Message = interaction.message
    except Exception as e:
        exceptionstring = format_exc()
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

class bjd_prev_next(discord.ui.View):
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

#Utility command to fix embeds of various BJD marketplace websites!
@client.slash_command(description="Command to fix embeds of some BJD websites! (check GitHub in bio for list of supported sites)")
async def bjd_embed(ctx: discord.Interaction, link: str):
    try:
        if "acbjd.com" in link:
            reqs = requests.get(link)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            
            main_image_div = soup.find('div', id='productMainImage')
            main_image_element = main_image_div.find('img')
            main_image = f"https://www.acbjd.com/{main_image_element.get('src')}"
            img = [main_image]
            other_image_div = soup.find('div', class_='descriptimage')
            other_img_elements = other_image_div.find_all('img')
            for image in other_img_elements:
                image_link = image.get('src')
                img.append(image_link)

            title = soup.find('h1', id='productName').get_text()
            product_div = soup.find('div', id='productGeneral')
            try:
                normal_price = product_div.find('span', class_='normalprice').get_text().strip()
                special_price = product_div.find('span', class_='productSpecialPrice').get_text().strip()
                if len(special_price) > 1:
                    price = f"~~{normal_price}~~ {special_price}"
                else:
                    price = normal_price
            except AttributeError:
                price = product_div.find('h2', id='productPrices').get_text()
        elif "denverdoll.com" in link:
            reqs = requests.get(link)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            gallery_div = soup.find('div', class_="woocommerce-product-gallery__wrapper")
            images_elements = gallery_div.find_all('a')
            images = []
            for image_element in images_elements:
                images.append(image_element.get('href'))
            main_image = images[0]
            title = soup.find('h1', class_='product_title').get_text()
            product_div = soup.find('div', class_='summary entry-summary')
            price = product_div.find('span', class_='amount').get_text()
        elif "dolkbjd.com" in link:
            reqs = requests.get(link)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            main_image_div = soup.find('div', class_='product-image-main')
            main_image_element = main_image_div.find('img')
            main_image = f"https:{main_image_element.get('data-photoswipe-src')}"
            img = [main_image]
            title = soup.find('h1', class_='h2 product-single__title').get_text()
            price_split = soup.find('span', class_='product__price').get_text().split()
            for line in price_split:
                if "." in line:
                    price = line
        elif "janesdolland.com" in link:
            reqs = requests.get(link)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            gallery_div = soup.find('div', {"data-hook":"main-media-image-wrapper"})
            images_elements = gallery_div.find_all('img')
            images = []
            for image_element in images_elements:
                images.append(image_element.get('src'))
            main_image = str(images[0])
            main_image = main_image.split("/fill/")
            main_image = main_image[0] + "/fill/w_500,h_750,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/28d43e_69c206a2bf7443ce9e187310ad233f84~mv2.png"
            title = soup.find('h1', {"data-hook":"product-title"}).get_text()
            price_div = soup.find('div', {"data-hook":"product-price"})
            try:
                price = price_div.find('span', {"data-hook":"price-range-from"}).get_text()
            except AttributeError:
                try:
                    old_price = price_div.find('span', {"data-hook":"formatted-secondary-price"}).get_text().strip()
                    new_price = price_div.find('span', {"data-hook":"formatted-primary-price"}).get_text().strip()
                    price = f"~~{old_price}~~ {new_price}"
                except AttributeError:
                    price = price_div.find('span', {"data-hook":"formatted-primary-price"}).get_text().strip()
        member: discord.User = ctx.user
        embed = discord.Embed(title=title, url=link)
        embed.add_field(name="Price", value=price)
        embed.set_image(url=main_image)
        await ctx.respond(embed=embed)
    except Exception as e:
        exceptionstring = format_exc()
        await ctx.respond("An error has occurred! Please try again!")
        await report.send(f"<@120396380073099264>\n{exceptionstring}\nIn {ctx.guild.name}")

client.run(TOKEN)