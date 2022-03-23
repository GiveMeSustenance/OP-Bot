import os
import discord
import requests
import json
from discord.ext import commands
from discord.utils import get
from all_time_zones import time_zone_check
from replit import db
from keep_alive import keep_alive

client = discord.Client()

#del db["personal_times"]
#print(db["personal_times"])

defaultPublicTimeZones = [ #the hard coded time zones
 "America/New_York",
 "Asia/Singapore",
 "America/Toronto"
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
Gets the time of a specific time zone.
'''

def get_customTime(timeZone):
  response = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=" + timeZone)
  json_data = json.loads(response.text)
  #print(json_data)
  time = json_data['time']
  return(time)

#end get_customTime

'''
Parses a string to a boolean. Currently accepted values for true: 'true' '1'
Other values entered will return false.
'''

def parseBoolean(string):
  accepted = ['true', '1'] #add more values to your heart's content
  return (string.lower() in accepted)

#end parseBool

def update_publicTimeZones(timeZone): #adds time zones to the public time zone list
  if "publicTimeZone" in db.keys(): #if there is already things in the "publicTimeZone" key
    publicTimeZones = db["publicTimeZones"] #makes a temporary variable to manipulate
    publicTimeZones.extend(timeZone) #adds the time zone to the end of the variable
    db["publicTimeZones"] = publicTimeZones #sets the key to the updated variable
  else: # if the key does not already exist
    db["publicTimeZones"] = [timeZone] #makes the "publicTimeZones" key with the new time zone

#end update_publicTimeZones

def delete_publicTimeZones(timeZone): #removes time zones from the public time zone list
  publicTimeZones = db["publicTimeZones"] #makes a temporary variable to manipulate
  publicTimeZones.remove(timeZone) #deletes the time zone from the variable
  db["publicTimeZones"] = publicTimeZones #sets the key to the updated variable

#end delete_publicTimeZones

def add_personal_timezone(time_zone, user):
  user = str(user)
  #print(user)
  #print(time_zone)
  personal_time_zones = db["personal_times"]
  #print(personal_time_zones)
  personal_time_zones.append(user)
  #print(personal_time_zones)
  personal_time_zones.append(time_zone)
  #print(personal_time_zones)
  db["personal_times"] = personal_time_zones

def to_12h_time(time):
  hour = time[:2]
  minute = time[3:]
  hour = int(hour)
  period = " am"
  if hour > 12:
    hour = hour - 12
    period = " pm"
  if hour == 12:
    period = " pm"
  twelve_hour_time = str(hour) + ":" + minute + period
  return(twelve_hour_time)

@client.event 
async def on_ready(): #when the bot is ready
    print('Logged in as {0.user}'.format(client)) #prints to the console ----->
    channelID = client.get_channel(954875808047050752) #op-bot-status channel
    #await channelID.send("**OP Bot Online**")

    global dadMode #declaring the dadMode variable bc it was yelling at me in the check  
    dadMode = 0
    print("when the bot loads up: ", defaultPublicTimeZones)

    if "personal_times" not in db.keys():
      db["personal_times"] = [" "]

'''
@client.event #adds and removes roles on message reaction (broken)
async def on_raw_reaction_add(payload):
  guild = client.get_guild(payload.guild_id)
  print(guild)
  #print("Reaction added: ", payload)
  if payload.channel_id == 913704059758845952: #roles channel
    print("-----\nRoles\n-----")
    if payload.emoji.id == 914002544601231390: #:pigman: emoji
      print("-----\nPigman\n-----")
      role = discord.utils.get(guild.roles, name="Pigman")
      await payload.member.add_roles(role)
 
@client.event
async def on_raw_reaction_remove(reaction):
  guild = discord.utils.find(lambda g: g.id == reaction.guild_id, bot.guilds)
  if reaction.channel_id == 913704059758845952: #roles channel
    if reaction.emoji.id == 914002544601231390: #:pigman: emoji
      role = discord.utils.get(guild.roles, name="Pigman")
      member = discord.utils.find(lambda m: m.id == reaction.user_id, guild.members)
      if member is not None:
        await member.remove_roles(role)
      
  print("Reaction removed")
'''

@client.event
async def on_message(message): #when a message is sent to the discord server
  
  allTimeZones = defaultPublicTimeZones #resets allTimeZones to the defualt hard coded zones
  if "publicTimeZones" in db.keys(): #if there is anything in the "publicTimeZones" key
    allTimeZones = allTimeZones + list(db["publicTimeZones"]) #adds the list to allTimeZones to reflect the changes
    #print("defaultPublicTimeZones", defaultPublicTimeZones)
    #print("publicTimeZones:", list(db["publicTimeZones"]))
    #print("allTimeZones:", allTimeZones, "\n")
    
  if message.author == client.user: #if the bot sent the message
    return #dont do anything

  ''' 
  Sends a list of current commands and their arguments on command
  ''' 
  
  if message.content.lower().startswith('!ophelp'): #if the message starts with "!ophelp" (not case sensitive bc it sets all characters to lowercase --> .lower() )
    await message.channel.send("**Current commands:**\n!ophelp\n!timein [time zone]\n!timezones\n!times\n!addtimezone [time zone] (no quotes)\n!deltimezone [time zone] (no quotes)\n!findtimezones (list of valid time zones)\n!dadmode [true/false]\n!github") #sends a hard coded list of commands

#end !ophelp

  if message.content.lower().startswith("!findtimezones"): #if the message starts with "!github"
    await message.channel.send("A list of time zones can be found at https://www.timeapi.io/api/TimeZone/AvailableTimeZones") #sends the link
  
  updateRoles = 0
  
  if updateRoles == 1:
    if message.content.lower().startswith("!updaterolechannel"):
      channelID = client.get_channel(913704059758845952) #roles channel
      await channelID.send("**React with the emoji to get the role and be notified when it is pinged**\nPoll Taker: <:heart:916441840633393202>\nForge Lover: <:fight:914004603647955064>\nGorge Lover: <:farm:916441731090767903>\nRat Hater (Uncompromising Mode): <:skull:916113183553507358>\nTerraria Enthusiast: <:shovel:916432312642728036>\n")
  
  global dadMode

  '''
  Toggles Dad Mode (on/off)
  '''

  if message.content.lower().startswith("!dadmode"): #if the message starts with "!dadmode"
    dadToggle = message.content[9:] #takes the text after "!dadmode" ie (true/false)
    dadMode = parseBoolean(dadToggle)
    if dadMode == True:
      await message.channel.send("Dad mode enabled") #sends "Dad mode enabled" to discord
    else:
      await message.channel.send("Dad mode disabled") #sends "Dad mode disabled" to discord
  
  if dadMode == True: #if dadMode is true (on)
    if message.content.lower().startswith("im"): #if the message starts with "im"
      dadMessage = message.content[3:] #takes the text after "im" and saves as a new string
      await message.channel.send("Hi " + dadMessage + ", I'm OP Bot") #sends msg to discord

#end !dadmode

  '''
  Prints the GitHub link on command
  '''
  
  if message.content.lower().startswith("!github"): #if the message starts with "!github"
    await message.channel.send("https://github.com/GiveMeSustenance/OP-Bot") #sends the link

#end !github

  '''
  Prints time of a specific input time zone on command
  '''
  
  if message.content.lower().startswith('!timein'): #if the message starts with "!time"
    input = message.content #saves message as a string
    if input.find(' ') != -1 and len(input) >= 5: #checks to make sure it contains a space
      customZone = message.content[8:] #takes the text after "!time" and saves as a new string
      print("customZone: " + customZone) #prints the string to the console for troubleshoting --->
      time = get_customTime(customZone) #sends "customZone" the function "get_customTime" (above) and gets the time back
      print("time: " + time) #prints the string to console
      time = to_12h_time(time)
      await message.channel.send("It is " + time + " in " + customZone)
    else: #if there is no space
      await message.channel.send("Please add a time zone: \n!addtimezone America/New_York \na list can be found at https://www.timeapi.io/api/TimeZone/AvailableTimeZones") #asks for a time zone and shows the syntax

  if message.content.lower().startswith('!timezones'): #if the message starts with "!alltimezones"
    await message.channel.send("**All Time Zones:**")
    for i in range(0, len(allTimeZones)):
      await message.channel.send(str(i + 1) + ": " + str(allTimeZones[i]))

  if message.content.lower().startswith('!addtimezone'): #if the message starts with "!addtimezone"
    newTimeZone = message.content[13:] #takes the text after "!addtimezone" and saves as a new string
    if newTimeZone in time_zone_check:
      if newTimeZone not in allTimeZones:
        print(newTimeZone) #prints it to the console
        update_publicTimeZones(newTimeZone) #sends "newTimeZone" the function "update_publicTimeZones" (above) which adds "newTimeZone" to the list of saved time zones
        await message.channel.send(newTimeZone + " was added to the public time zones!") #sends a discord message to show it was added
      else:
        await message.channel.send(newTimeZone + " is alredy added")
    else:
      await message.channel.send("That is not a valid time zone. Please pick one from https://www.timeapi.io/api/TimeZone/AvailableTimeZones (do not include quotes)")

  if message.content.lower().startswith('!deltimezone'): #if the message starts with "!deltimezone"
    delTimeZone = message.content[13:] #takes the text after "!deltimezone" and saves as a new string
    if "publicTimeZones" in db.keys() and (delTimeZone in list(db["publicTimeZones"])): #if "publicTimeZones" exists (there is something in it)
      delete_publicTimeZones(delTimeZone) #sends "delTimeZone" the function "delete_publicTimeZones" (above) which removes "delTimeZone" from the list of saved time zones
      await message.channel.send(delTimeZone + " has been deleted") #sends the list of remaining time zones in discord (broken rn)
    else:
      await message.channel.send('"' + delTimeZone + '"' + " is not in the list of time zones")
      
  if message.content.lower().startswith('!times'): #sends the current time for all saved time zones in the "publicTimeZones" list
    publicZoneString = " ".join(allTimeZones)

    tempZoneList = publicZoneString.split(" ")
    for i in range(len(allTimeZones)):
      tempTimeZone = tempZoneList[i]
      print(tempZoneList[i])
      tempTime = get_customTime(tempTimeZone)
      twelve_hour_time = to_12h_time(tempTime)
      await message.channel.send("It is " + twelve_hour_time + " in " + tempTimeZone)

  if message.content.lower().startswith('!myzone'):
    timeZone = message.content[8:]
    print(timeZone)
    if timeZone in time_zone_check:
      if str(message.author) not in list(db["personal_times"]):
        user_id = message.author
        add_personal_timezone(timeZone, user_id)
        print(db["personal_times"])
      else:
        await message.channel.send("you have already registered a time zone")
    else:
      await message.channel.send("that is not a valid time zone")
      
  if message.content.lower().startswith('!mytime'):
    if str(message.author) in list(db["personal_times"]):
      index = list(db["personal_times"]).index(str(message.author))
      time_zone = db["personal_times"][index + 1]
      time = get_customTime(time_zone)
      await message.channel.send("it is " + time + " in " + time_zone)
    else:
      await message.channel.send("you do not have a time zone")

    
keep_alive() #keeps the bot running by pinging the web server
client.run(os.environ['Bot Token']) #allows the program to connect to the bot
