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
versionnum = "3.0b"
updatetime = "2024/02/05 21:14"
changes = "**(3.0b)** Added a reputation giving function that includes a function to look at your reputation and who's given you/who you've given the most reputation\n(a) Dramatically decreased chances of Google search and Grumpy Bedtime images in meme gen\(b) Fixed update time syntax"
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

with open(f'{path}\\rep.json',"r+") as file:
    try:
        text = json.loads(file.read())
        rep = text
        print(rep)
    except JSONDecodeError as e:
        print(e)
        rep = {}
    file.close()

with open(f'{path}\\totalrep.json',"r+") as file:
    try:
        text = json.loads(file.read())
        totalrep = text
        print(f"totalrep: {totalrep}")
    except JSONDecodeError as e:
        print(e)
        totalrep = {}
    file.close()

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
        
wikis = ["mario","minecraft","fanon","ssb"]
mariowiki = ["https://www.mariowiki.com/index.php?title=Category:Character_artwork&fileuntil=AlolanExeggutorUltimate.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=AlolanExeggutorUltimate.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Back-To-School+Funny+Personality+Quiz+result+Toadette.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Black+Kirby+SSBU.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Boomgtt.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Box+Art+Background+-+Mario+Party+Island+Tour.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Captain+toad-+New+Donk+City+bg.jpg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Club+Nintendo+Mario+German+Flag.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Daisy+MPIT.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Ditrani+Salvatore+MRSOH+Midnite.jpg#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DKC2+Screech.png#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DMW+Skill+Summit+12+mentors.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Donkey+Kong+vector+art.svg#mw-category-media","https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=DrMarioLesson.png#mw-category-media",
             "https://www.mariowiki.com/index.php?title=Category:Character_artwork&filefrom=Fire+Mario.png#mw-category-media"]
mcwiki = ["https://minecraft.wiki/w/Category:Mojang_images","https://minecraft.wiki/w/Category:Mojang_images?filefrom=1-18-dripstone-caves.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=1.19.1-pre3.jpg#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=11a-44.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=14w31a+textures+0.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=2+joined+shipwrecks.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=21a01-25.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=3inone.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Abominable+Weaver+Icon.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Acacia+Sign+JE1+BE1.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Adriene+Texture+%28MCD%29.png#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Albino+Cow+Spawn+Egg+Icon.png#mw-category-media",
          "https://minecraft.wiki/w/Category:Mojang_images?filefrom=Allay+animated+sticker.gif#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Alpha+v1.2.1.jpg#mw-category-media","https://minecraft.wiki/w/Category:Mojang_images?filefrom=Ancient+City+intact+corner+wall+1.png#mw-category-media"]
ssb = ["https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230614074616&limit=500",
       "https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230211232543&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20230126182127&limit=500",
       "https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20211005224641&limit=500","https://supersmashbros.fandom.com/wiki/Special:NewFiles?offset=20210703010151&limit=500"]
stringlist = {}
aff = ["Okay", "Alright", "Got it", "Affirmative","Sounds good"]
selfrep = ["You're giving reputation to me-Q?? Well, thank you-Q! ^^","Oh...thank you so much for the reputation-Q! I will take good care of it-Q! ^^"]
bots = [432610292342587392, 429305856241172480, 439205512425504771, 247283454440374274, 431544605209788416]
guilds = [783976468815937556,1032727370584559617,467886334971871232,645086582755557396]
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
        "’":"'",
        "“":'"',
        "”":'"'
    }
    for key, value in formatlist.items():
        text = text.replace(key, value)
    return text

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"{status}"))
    print('Bot is online!')

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "🏅":
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

        # Ensure totalrep structure exists
        if guild_id_str not in totalrep:
            totalrep[guild_id_str] = {}
        if author_id_str not in totalrep[guild_id_str]:
            totalrep[guild_id_str][author_id_str] = 0

        # Update totalrep
        totalrep[guild_id_str][author_id_str] += 1

        await reaction.message.channel.send(f"<@{user_id_str}> has given <@{author_id_str}> +1 reputation-Q!")

        # Write to files
        with open(f'{path}\\rep.json', "w") as file:
            json.dump(rep, file)
        
        with open(f'{path}\\totalrep.json', "w") as file:
            json.dump(totalrep, file)

    

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
    if "||" in message.content:
        return
    try:
        msglist = stringlist[str(message.guild.id)]
        if len(msglist) > 100:
            msglist = msglist[-30:0]
        msglist.append(message.content)
        stringlist[str(message.guild.id)] = msglist
    except KeyError:
        stringlist.update({str(message.guild.id):[message.content]})
    print(stringlist)

@client.slash_command(description="Returns XyL-Q version number!", guild_ids=guilds)
async def version(ctx): 
    await ctx.respond(f"Hello-Q! I'm XyL-Q, running version {versionnum} released on {updatetime}-Q!")

@client.slash_command(description="Shows you your reputation and other related stats!")
async def reputation(ctx):
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


@client.slash_command(description="Disables message caching in a given channel or from a given user!", guild_ids=guilds)
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

@client.slash_command(description="Disables a command in a given channel!", guild_ids=guilds)
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

@client.slash_command(description="Makes a meme based on parameters given!", guild_ids=guilds)
async def meme(ctx, top_text=None, bottom_text=None, image_link=None, image_upload: discord.Attachment=None): 
        if (top_text == None) and (bottom_text != None):
            top_text = random.choice(stringlist[str(ctx.guild.id)])
        if (bottom_text == None) and (top_text != None):
            bottom_text = random.choice(stringlist[str(ctx.guild.id)])
        if (bottom_text == None) and (top_text == None):
            #everybody say thaaaank you chatGPT
            full_text = random.choice(stringlist[str(ctx.guild.id)])

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
            if image_upload != None:
                image_link = image_upload.url
            elif image_upload == None:
                numba = random.choice(range(11))
                if numba > 10:
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
                elif numba < 1:
                    image_link = random.choice(imglist)
                else:
                    wiki = random.choice(wikis)
                    if wiki == "mario":
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
                    if wiki == "minecraft":
                        url = random.choice(mcwiki)
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
                        image_link = f"https://minecraft.wiki{random.choice(urls)}"
                    if wiki == "fanon":
                        url = "https://carebearsfanon.fandom.com/wiki/Special:NewFiles?offset=&limit=500"
                        reqs = requests.get(url)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if url[-4:] == ".png":
                                    if "File:" in url:
                                        urls.append(url)
                        page = f"https://carebearsfanon.fandom.com{random.choice(urls)}"
                        reqsagain = requests.get(page)
                        soup = BeautifulSoup(reqsagain.text, 'html.parser')
                        
                        urls = []
                        for link in soup.find_all('a'):
                            url = link.get('href')
                            if url != None:
                                if ".png" in url:
                                    print(url)
                                    if "images" in url:
                                        urls.append(url)
                        image_link = random.choice(urls)
                    if wiki == "ssb":
                        url = url = random.choice(ssb)
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
                                    print(url)
                                    if "images" in url:
                                        urls.append(url)
                        image_link = random.choice(urls)

        memelink = f"https://api.memegen.link/images/custom/{top_text_new}/{bottom_text_new}.png?background={image_link}"
        await ctx.respond(memelink)

client.run(TOKEN)