import os
import discord
import requests
import json
from discord.ext import commands
from all_time_zones import time_zone_check
from replit import db
from keep_alive import keep_alive
import random

client = discord.Client()

bot = commands.Bot(command_prefix='!')

#del db["personal_times"]
#print(db["personal_times"])

#del db["time_response_toggle"]
#print(db["time_response_toggle"])

dad_toggle = False

default_public_time_zones = [ #the hard coded time zones
 "Asia/Singapore",
 "America/Toronto"
]

shut_down_phrases = [
  ""
]

trigger_phrases = [
  
]

'''
Discord Channel IDs:
roles: 913704059758845952
op-bot-status: 954875808047050752

Emoji IDs:
:Pigman: 914002544601231390
:fight: 914004603647955064
:farm: 916441731090767903
:shovel: 916432312642728036
:skull: 916113183553507358
:heart: 916441840633393202
'''

'''
converts the input time to another time zone
'''

def convert_time(request_body):
  response = requests.post("https://www.timeapi.io/api/Conversion/ConvertTimeZone", json = request_body)
  json_data = json.loads(response.text)
  converted_time = json_data['conversionResult']['time']
  return(converted_time)

#end convert_time

'''
Gets the dateTime of a specific time zone - closer in proper form than 'date' to be used in convert_time()
'''

def get_dateTime(time_zone):
  response = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=" + time_zone)
  json_data = json.loads(response.text)
  dateTime = json_data["dateTime"]
  return(dateTime)

#end get_dateTime

'''
Gets the time of a specific time zone
'''

def get_custom_time(timeZone):
  response = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=" + timeZone)
  json_data = json.loads(response.text)
  time = json_data['time']
  return(time)

#end get_custom_time

'''
Parses a string to a boolean
Strings in list(accepted) return true
Other values entered will return false
'''

def parse_boolean(string):
  accepted = ['true', '1']
  return (string.lower() in accepted)

#end parseBool

'''
adds a new time zone to the list of public time zones
'''

def update_public_time_zones(timeZone):
  if "publicTimeZone" in db.keys():
    publicTimeZones = db["publicTimeZones"]
    publicTimeZones.extend(timeZone)
    db["publicTimeZones"] = publicTimeZones
  else:
    db["publicTimeZones"] = [timeZone]

#end update_public_time_zones

'''
deletes a time zone from the list of public time zones
'''

def delete_public_time_zone(timeZone):
  publicTimeZones = db["publicTimeZones"]
  publicTimeZones.remove(timeZone)
  db["publicTimeZones"] = publicTimeZones

#end delete_public_time_zone

'''
adds the user and a time zone to the list of personal time zones
'''

def add_personal_time_zone(time_zone, user):
  user = str(user)
  if "personal_times" in db.keys():
    personal_time_zones = db["personal_times"]
    personal_time_zones.append(user)
    personal_time_zones.append(time_zone)
    db["personal_times"] = personal_time_zones
  else:
    db["personal_times"] = user
    personal_time_zones = db["personal_times"]
    personal_time_zones.append(time_zone)
    db["personal_times"] = personal_time_zones

#end add_personal_time_zone

'''
converts a time to twelve hour and returns it
'''

def to_12h_time(time):
  hour = time[:2]
  print(hour)
  minute = time[3:]
  print(minute)
  hour = int(hour)
  period = " am"
  if hour == 24:
    hour -= 12
    period = " am"
  elif hour > 12:
    hour -= 12
    period = " pm"
  elif hour == 12:
    period = " pm"
  twelve_hour_time = str(hour) + ":" + minute + period
  return(twelve_hour_time)

#end to_12h_time

@client.event 
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    channelID = client.get_channel(954875808047050752) #op-bot-status channel
    #await channelID.send("**OP Bot Online**")

@client.event
async def on_raw_reaction_add(payload):
  
  emoji_id = payload.emoji.id
  
  if payload.channel_id == 913704059758845952: #roles channel
    member = payload.member
    
    if emoji_id == 914002544601231390: #:pigman: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Pigman")
      
    elif emoji_id == 914004603647955064: #:fight: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Forge Lovers")
      
    elif emoji_id == 916441731090767903: #:farm: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Gorge Lovers")
      
    elif emoji_id == 916113183553507358: #:skull~1: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Rat Hater")
      
    elif emoji_id == 916432312642728036: #:shovel: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Terraria Enthusiast")
      
    elif emoji_id == 916441840633393202: #:shovel: emoji
      role = discord.utils.get(payload.member.guild.roles, name = "Poll Taker")
      
    await member.add_roles(role)
 
@client.event
async def on_raw_reaction_remove(payload):

  emoji_id = payload.emoji.id
  
  if payload.channel_id == 913704059758845952: #roles channel
    guild = await client.fetch_guild(payload.guild_id)
    member = await guild.fetch_member(payload.user_id)
    
    if emoji_id == 914002544601231390: #:pigman: emoji
      role = discord.utils.get(guild.roles, name = "Pigman")
      
    elif emoji_id == 914004603647955064: #:fight: emoji
      role = discord.utils.get(guild.roles, name = "Forge Lovers")
      
    elif emoji_id == 916441731090767903: #:farm: emoji
      role = discord.utils.get(guild.roles, name = "Gorge Lovers")
      
    elif emoji_id == 916113183553507358: #:skull~1: emoji
      role = discord.utils.get(guild.roles, name = "Rat Hater")
      
    elif emoji_id == 916432312642728036: #:shovel: emoji
      role = discord.utils.get(guild.roles, name = "Terraria Enthusiast")
      
    elif emoji_id == 916441840633393202: #:shovel: emoji
      role = discord.utils.get(guild.roles, name = "Poll Taker")
      
    await member.remove_roles(role)

@client.event
async def on_message(message):

  discord_message = message.content
  
  all_time_zones = default_public_time_zones
  if "publicTimeZones" in db.keys():
    all_time_zones = all_time_zones + list(db["publicTimeZones"])
    
  if message.author == client.user:
    return

# ------------------------------------------------------------------------------------------------------------------------------------------------

  ''' 
  Sends a list of current commands and their arguments on command
  ''' 

  command_help = {
    "ophelp": "lists of all commands the bot can do",
    "timein": "finds the current time in a specified time zone: !timein America/Toronto",
    "timezones": "sends all the time zones the bot is storing",
    "times": "sends the current times in all time zones the bot is storing",
    "addtimezone": "adds a time zone to the bot's list: !addtimezone America/Toronto",
    "deltimezone": "deletes a time zone from the bots list: !deltimezone America/Toronto",
    "findtimezones": "links a map to find valid time zones",
    "myzone": "sets a personal time zone to use with !mytime, !convert, and automatic time responses: !myzone America/Toronto",
    "mytime": "sends the time in your personal time zone",
    "pigman": "gives you the pigman role",
    "convert": "converts a 24 hour time from your personal time zone to all time zones in the bot's list: !convert 13:00",
    "roll": "rolls a random number. Add a number after to roll between 0 and that number (default 100): !roll or !roll 420",
    "coinflip": "flips a coin and tells you how it lands",
    "dadmode": "toggles dad mode (Hi hungry, I'm dad!): !dadmode true/false",
    "github": "sends the link to the github page with all the bot's code",
    "timeresponse": "toggles whether the bot will convert times you post in chat to time zones from its list"
  }
  
  if discord_message.lower().startswith('!ophelp'):
    if discord_message[8:].strip() == "":
      await message.channel.send("**Help Commands:**\n!ophelp\n\n**Time Commands:**\n!timein [time zone]\n!timezones\n!times\n!addtimezone [time zone]\n!deltimezone [time zone]\n!findtimezones\n!myzone [time zone]\n!mytime\n!convert [time]\n!timeresponse [true/false]\n\n**Fun Commands**\n!pigman\n!roll\n!coinflip\n!dadmode [true/false]\n!github\n\n**Need more info? do !ophelp [command] (!ophelp times)**")
    else:
      print(discord_message[8:])
      await message.channel.send("!" + discord_message[8:] + " " + command_help[discord_message[8:]])


    
#end !ophelp --------------------------------------------------------------------------------------------------------------------------------------

  if discord_message.lower().startswith('!pigman'):
    member = message.author
    print(member)
    var = discord.utils.get(message.guild.roles, name = "Pigman")
    await member.add_roles(var)

#end !pigman --------------------------------------------------------------------------------------------------------------------------------------
  
  if discord_message.lower().startswith("!findtimezones"):
    await message.channel.send("A list of time zones can be found at https://www.timeapi.io/Tools/TimeZoneMap")

#end !findtimezones -------------------------------------------------------------------------------------------------------------------------------
  
  updateRoles = 0
  
  if discord_message.lower().startswith("!updaterolechannel") and updateRoles == 1:
    channelID = client.get_channel(913704059758845952) #roles channel
    await channelID.send("**React with the emoji to get the role and be notified when it is pinged**\nPoll Taker: <:heart:916441840633393202>\nForge Lover: <:fight:914004603647955064>\nGorge Lover: <:farm:916441731090767903>\nRat Hater (Uncompromising Mode): <:skull:916113183553507358>\nTerraria Enthusiast: <:shovel:916432312642728036>\n")
  
#end !updaterolechannel ---------------------------------------------------------------------------------------------------------------------------

  '''
  Toggles Dad Mode (on/off)
  '''
  if discord_message.lower().startswith("!dadmode"):
    global dad_toggle
    dad_toggle = discord_message[9:]
    dad_toggle = parse_boolean(dad_toggle)
    if dad_toggle == True:
      await message.channel.send("Dad mode enabled")
    else:
      await message.channel.send("Dad mode disabled")
  
  if dad_toggle == True:
    if discord_message.lower().startswith("im"):
      dadMessage = discord_message[3:]
      await message.channel.send("Hi " + dadMessage + ", I'm OP Bot")

#end !dadmode -------------------------------------------------------------------------------------------------------------------------------------

  '''
  Prints the GitHub link on command
  '''
  
  if discord_message.lower().startswith("!github"):
    await message.channel.send("https://github.com/GiveMeSustenance/OP-Bot")

#end !github --------------------------------------------------------------------------------------------------------------------------------------

  if discord_message.lower().startswith("!roll"):
    max_range = 100
    custom_range = discord_message[6:]
    if len(custom_range) > 0 and custom_range.isnumeric():
      max_range = int(custom_range)
    roll_number = str(random.randint(0,max_range))
    await message.channel.send(message.author.mention + " rolls " + roll_number)

#end !roll ----------------------------------------------------------------------------------------------------------------------------------------

  '''
  Prints time of a specific input time zone on command
  '''
    
  if discord_message.lower().startswith('!timein'):
    input = discord_message
    if input.find(' ') != -1 and len(input) >= 5:
      customZone = discord_message[8:]
      time = get_custom_time(customZone)
      time = to_12h_time(time)
      await message.channel.send("It is " + time + " in " + customZone)
    else:
      await message.channel.send("Please add a time zone: \n!addtimezone America/New_York \na list can be found at https://www.timeapi.io/Tools/TimeZoneMap")

#end !timein ---------------------------------------------------------------------------------------------------------------------------------------
  
  '''
  Prints all saved time zones on command
  '''
  
  if discord_message.lower().startswith('!timezones'): #if the message starts with "!alltimezones"
    await message.channel.send("**All Time Zones:**")
    for i in range(0, len(all_time_zones)):
      await message.channel.send(str(i + 1) + ": " + str(all_time_zones[i]))

#end !timezones -----------------------------------------------------------------------------------------------------------------------------------

  '''
  adds a time zone to the saved public list on command
  '''
  
  if discord_message.lower().startswith('!addtimezone'): #if the message starts with "!addtimezone"
    newTimeZone = discord_message[13:] #takes the text after "!addtimezone" and saves as a new string
    if newTimeZone in time_zone_check:
      if newTimeZone not in all_time_zones:
        print(newTimeZone) #prints it to the console
        update_public_time_zones(newTimeZone) #sends "newTimeZone" the function "update_public_time_zones" (above) which adds "newTimeZone" to the list of saved time zones
        await message.channel.send(newTimeZone + " was added to the public time zones!") #sends a discord message to show it was added
      else:
        await message.channel.send(newTimeZone + " is alredy added")
    else:
      await message.channel.send("That is not a valid time zone. Please pick one from https://www.timeapi.io/Tools/TimeZoneMap (do not include quotes)")

#end !addtimezone --------------------------------------------------------------------------------------------------------------------------------

  '''
  deletes a time zone from the saved public list on command
  '''
  
  if discord_message.lower().startswith('!deltimezone'): #if the message starts with "!deltimezone"
    delTimeZone = discord_message[13:] #takes the text after "!deltimezone" and saves as a new string
    if "publicTimeZones" in db.keys() and (delTimeZone in list(db["publicTimeZones"])): #if "publicTimeZones" exists (there is something in it)
      delete_public_time_zone(delTimeZone) #sends "delTimeZone" the function "delete_public_time_zone" (above) which removes "delTimeZone" from the list of saved time zones
      await message.channel.send(delTimeZone + " has been deleted") #sends the list of remaining time zones in discord (broken rn)
    else:
      await message.channel.send('"' + delTimeZone + '"' + " is not in the list of time zones")

#end !deltimezone ---------------------------------------------------------------------------------------------------------------------------------

  '''
  sends the times in all saved public time zones to discord on command
  '''
      
  if discord_message.lower().startswith('!times'): #sends the current time for all saved time zones in the "publicTimeZones" list
    publicZoneString = " ".join(all_time_zones)

    tempZoneList = publicZoneString.split(" ")
    for i in range(len(all_time_zones)):
      tempTimeZone = tempZoneList[i]
      print(tempZoneList[i])
      tempTime = get_custom_time(tempTimeZone)
      twelve_hour_time = to_12h_time(tempTime)
      await message.channel.send("It is " + twelve_hour_time + " in " + tempTimeZone)

#end !times ---------------------------------------------------------------------------------------------------------------------------------------

  '''
  saves a personal time zone for the user in a list (user, time zone) on command
  '''
  
  if discord_message.lower().startswith('!myzone'):
    timeZone = discord_message[8:]
    print(timeZone)
    if timeZone in time_zone_check:
      if str(message.author) not in list(db["personal_times"]):
        user_id = message.author
        add_personal_time_zone(timeZone, user_id)
        print(db["personal_times"])
      else:
        await message.channel.send("you have already registered a time zone")
    else:
      await message.channel.send("that is not a valid time zone")

#end !myzone --------------------------------------------------------------------------------------------------------------------------------------

  '''
  sends the time in the users personal time zone to discord on command
  '''
      
  if discord_message.lower().startswith('!mytime'):
    if str(message.author) in list(db["personal_times"]):
      index = list(db["personal_times"]).index(str(message.author))
      time_zone = db["personal_times"][index + 1]
      time = get_custom_time(time_zone)
      time = to_12h_time(time)
      await message.channel.send("it is " + time + " in " + time_zone)
    else:
      await message.channel.send("you do not have a time zone")

#end !mytime --------------------------------------------------------------------------------------------------------------------------------------

  '''
  toggles whether the bot responds to times mentioned by the user in discord
  '''
  
  if discord_message.lower().startswith("!timeresponse"):
    true_false = discord_message[14:]
    true_false = parse_boolean(true_false)
    author = str(message.author)
    if "time_response_toggle" in db.keys():
      print("in keys")
      if true_false == True:
        print("true")
        if author not in db["time_response_toggle"]:
          print(author + ' not in db["time_response_toggle"]')
          db["time_response_toggle"].append(author)
          await message.channel.send("Time responses enabled")
        else:
          await message.channel.send("You have already enabled this")
      else:
        if author in db["time_response_toggle"]:
          db["time_response_toggle"].remove(author)
          await message.channel.send("Time responses disabled")
        else:
          await message.channel.send("you have already disabled this")
    else:
      if true_false == True:
        print("not in keys")
        db["time_response_toggle"] = []
        db["time_response_toggle"].append(author)
        print(db["time_response_toggle"])
        await message.channel.send("Time responses enabled")
      else:
        await message.channel.send("you have already disabled this")
      
#end !timeresponse --------------------------------------------------------------------------------------------------------------------------------

  '''
  responds to times mentioned in discord (only 12 hour with an am/pm) and sends the corresponding time in all saves public time zones
  '''
  
  if str(message.author) in db["time_response_toggle"] and not discord_message.startswith("!") and any(char.isdigit() for char in discord_message):
    index = [char.isdigit() for char in discord_message].index(True)
    display_time = discord_message[index]
    time = discord_message[index]
    if discord_message[index + 1].isdigit(): #allows for 2 digit times
      print("2-digit")
      time = discord_message[index:index + 2]
    contains_am_pm = discord_message[index:index + 8].lower()
    if "am" in contains_am_pm or "pm" in contains_am_pm:
      if "am" in contains_am_pm:
        print("has am")
        am_pm = "am"
      elif "pm" in contains_am_pm:
        print("has pm")
        am_pm = "pm"
      if str(message.author) in list(db["personal_times"]):
        print("personal time zone exists")
        personal_time_zone_index = list(db["personal_times"]).index(str(message.author)) + 1
        author_time_zone = db["personal_times"][personal_time_zone_index]
      
        date_time = get_dateTime(author_time_zone)
        date = date_time[:10]
        if am_pm == "pm":
          time = int(time) + 12
        if int(time) < 10:
          time = "0" + time
        time = str(time) + ":00:00"
        date_time = date + " " + time
        
        for i in range(len(all_time_zones)):
          to_time_zone = all_time_zones[i]
          request_body = {
            "fromTimeZone": author_time_zone,
            "dateTime": date_time,
            "toTimeZone": to_time_zone,
            "dstAmbiguity": ""
          }
          #print(request_body)
          converted_time = convert_time(request_body)
          print(converted_time)
          converted_time = to_12h_time(converted_time)
          await message.channel.send(display_time + " " + am_pm + " in **" + author_time_zone + "** is " + converted_time + " in **" + to_time_zone + "**")
      else:
        await message.channel.send("Add a personal time zone with **!myzone [time zone]** to allow for auto replies")

#end time responder -------------------------------------------------------------------------------------------------------------------------------
  if discord_message.lower().startswith("!convert"):
    time = discord_message[9:]
    time = to_12h_time(time)
    await message.channel.send(time)

#end time responder -------------------------------------------------------------------------------------------------------------------------------

  if discord_message.lower().startswith("!coinflip"):
    flip_result = random.randint(0,1)
    if flip_result == 0:
      flip_result = "Heads"
    else:
      flip_result = "Tails"
    await message.channel.send("It's " + flip_result + "!")

#end time !coinflip -------------------------------------------------------------------------------------------------------------------------------
    
  #checks if the message contains the skull emoji
  if "<:skull:916113183553507358>" in discord_message: 
    #if found at least once, send funny skeletons gif
    await message.channel.send("https://tenor.com/view/sans-undertale-papyrus-gif-10107813")

#end papyrus-sans gif appender -----------------------------------------------------------------------
    
keep_alive() #keeps the bot running by pinging the web server
client.run(os.environ['Bot Token']) #allows the program to connect to the bot
