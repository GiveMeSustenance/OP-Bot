import os
import discord
import requests
import json
from replit import db
from keep_alive import keep_alive

client = discord.Client()

defaultPublicTimeZones = [ #the hard coded time zones
 "America/New_York",
 "Asia/Singapore",
 "America/Toronto"
]

allTimeZones = defaultPublicTimeZones #resets allTimeZones to the defualt hard coded zones
if "publicTimeZones" in db.keys(): #if there is anything in the "publicTimeZones" key
  allTimeZones.extend(db["publicTimeZones"]) #adds it to the end of allTimeZones to reflect the changes

def get_customTime(customZone): #returns the time at the provided time zone
  response = requests.get("https://www.timeapi.io/api/Time/current/zone?timeZone=" + customZone)
  json_data = json.loads(response.text) #honestly idk
  time = json_data['time'] #pulling a specific part of the data (the time)
  return(time)

def update_publicTimeZones(timeZone): #adds time zones to the public time zone list
  if "publicTimeZone" in db.keys(): #if there is already things in the "publicTimeZone" key
    publicTimeZones = db["publicTimeZones"] #makes a temporary variable to manipulate
    publicTimeZones.extend(timeZone) #adds the time zone to the end of the variable
    db["publicTimeZones"] = publicTimeZones #sets the key to the updated variable
    
    allTimeZones = defaultPublicTimeZones #resets allTimeZones to the defualt hard coded zones
    if "publicTimeZones" in db.keys(): #if there is anything in the "publicTimeZones" key
      allTimeZones.extend(db["publicTimeZones"]) #adds it to the end of allTimeZones to reflect the changes
  else: # if the key does not already exist
    db["publicTimeZones"] = [timeZone] #makes the "publicTimeZones" key with the new time zone
    allTimeZones = defaultPublicTimeZones #resets allTimeZones to the defualt hard coded zones
    if "publicTimeZones" in db.keys(): #if there is anything in the "publicTimeZones" key
      allTimeZones.extend(db["publicTimeZones"]) #adds it to the end of allTimeZones to reflect the changes

def delete_publicTimeZones(timeZone): #removes time zones from the public time zone list
  publicTimeZones = db["publicTimeZones"] #makes a temporary variable to manipulate
  publicTimeZones.remove(timeZone) #deletes the time zone from the variable
  db["publicTimeZones"] = publicTimeZones #sets the key to the updated variable
  
  allTimeZones = defaultPublicTimeZones #resets allTimeZones to the defualt hard coded zones
  if "publicTimeZones" in db.keys(): #if there is anything in the "publicTimeZones" key
     allTimeZones.extend(db["publicTimeZones"]) #adds it to the end of allTimeZones to reflect the changes

@client.event 
async def on_ready(): #when the bot is ready
    print('Logged in as {0.user}'.format(client)) #prints to the console ----->

    global dadMode #declaring the dadMode variable bc it was yelling at me in the chesk  
    dadMode = 0

@client.event
async def on_message(message): #when a message is sent to the discord server
  if message.author == client.user: #if the bot sent the message
    return #dont do anything
    
  if message.content.lower().startswith('!ophelp'): #if the message starts with "!ophelp" (not case sensitive bc it sets all characters to lowercase --> .lower() )
    await message.channel.send("**Current commands:**\n!ophelp\n!time [time zone]\n!alltimezones\n!alltimes\n!dadmode [true/false]\n!github") #sends a hard coded list of commands

  global dadMode
  
  if message.content.lower().startswith("!dadmode"): #if the message starts with "!dadmode"
    dadToggle = message.content.split("!dadmode ",1 )[1] #takes the text after "!dadmode" ie (true/false)
    if dadToggle == "true": #if true
      dadMode = 1
      await message.channel.send("Dad mode enabled") #sends "Dad mode enabled" to discord
    if dadToggle == "false": #if false
      dadMode = 0
      await message.channel.send("Dad mode disabled") #sends "Dad mode disabled" to discord
  
  if dadMode == 1: #if dadMode is true (on)
    if message.content.lower().startswith("im"): #if the message starts with "im"
      dadMessage = message.content.split("im ",1)[1] #takes the text after "im" and saves as a new string
      dadMessage = dadMessage.split(" ", 1)[0] #takes the first word of the new string
      await message.channel.send("Hi " + dadMessage + ", I'm OP Bot") #sends msg to discord

  if message.content.lower().startswith("!github"): #if the message starts with "!github"
    await message.channel.send("https://github.com/GiveMeSustenance/OP-Bot") #sends the link
  
  if message.content.lower().startswith('!time'): #if the message starts with "!time"
    input = message.content #saves message as a string
    if input.find(' ') != -1: #checks to make sure it contains a space
      if len(input) >= 5: #checks to make sure its greater then or equal to 5 characters
        customZone = message.content.split("!time ",1)[1] #takes the text after "!time" and saves as a new string
        print("customZone: " + customZone) #prints the string to the console for troubleshoting --->
        time = get_customTime(customZone) #sends "customZone" the function "get_customTime" (above) and gets the time back
        timeString = str(time) #makes the integer from "get_customTime" into a string
        print("time: " + time) #prints the string to console
        await message.channel.send("It is " + timeString + " in " + customZone) #sends the time in a discord message
    else: #if there is no space
      await message.channel.send("Please add a time zone: \n!addtimezone America/New_York \na list can be found at https://www.timeapi.io/api/TimeZone/AvailableTimeZones") #asks for a time zone and shows the syntax

  if message.content.lower().startswith('!alltimezones'): #if the message starts with "!alltimezones"
    await message.channel.send(allTimeZones) #send the list of all the saved time zones

  if message.content.lower().startswith('!addtimezone'): #if the message starts with "!addtimezone"
    newTimeZone = message.content.split("!addtimezone ", 1)[1] #takes the text after "!addtimezone" and saves as a new string
    print(newTimeZone) #prints it to the console
    update_publicTimeZones(newTimeZone) #sends "newTimeZone" the function "update_publicTimeZones" (above) which adds "newTimeZone" to the list of saved time zones
    await message.channel.send(newTimeZone + " was added to the public time zones!") #sends a discord message to show it was added

  if message.content.lower().startswith('!deltimezone'): #if the message starts with "!deltimezone"
    if "publicTimeZones" in db.keys(): #if "publicTimeZones" exists (there is something in it)
      delTimeZone = message.content.split("!deltimezone ", 1)[1] #takes the text after "!deltimezone" and saves as a new string
      delete_publicTimeZones(delTimeZone) #sends "delTimeZone" the function "delete_publicTimeZones" (above) which removes "delTimeZone" from the list of saved time zones
      await message.channel.send("Remaining public time zones:") #sends the list of remaining time zones in discord (broken rn)
      await message.channel.send(allTimeZones)
      
  if message.content.lower().startswith('!alltimes'): #sends the current time for all saved time zones in the "publicTimeZones" list
    allPublicTimeZones = defaultPublicTimeZones
    if "publicTimeZones" in db.keys():
      allPublicTimeZones.extend(db["publicTimeZones"])
    publicZoneString = " ".join(allPublicTimeZones)
    for x in range(len(allPublicTimeZones)):
      tempTimeZone = publicZoneString.split(" ")[x]
      print(publicZoneString.split(" ")[x])
      tempTime = get_customTime(tempTimeZone)
      print("tempTimeZone: " + tempTimeZone)
      print("tempTime: " + tempTime)
      await message.channel.send("It is " + tempTime + " in " + tempTimeZone)

keep_alive() #keeps the bot running by pinging the web server
client.run(os.environ['Bot Token']) #allows the program to connect to the bot
