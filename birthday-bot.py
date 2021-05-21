from ics import Calendar
from common import initLogger
from dotenv import load_dotenv, find_dotenv
import requests
import logging
import discord
import os
import asyncio
import json
import arrow
import urllib.parse
from datetime import date, datetime, timedelta
from dateutil import tz
import random

log = initLogger.create(__name__)
load_dotenv(find_dotenv())

ICAL_URL = os.getenv("ICAL_URL")
if ICAL_URL == None:
    log.critical("No ICAL_URL environment variable is set.  Aborting...")
    exit(1)

DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
if DISCORD_CHANNEL_ID == None:
    log.critical("No DISCORD_CHANNEL_ID environment variable is set.  Aborting...")
    exit(1)

DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
if DISCORD_GUILD_ID == None:
    log.critical("No DISCORD_GUILD_ID environment variable is set.  Aborting...")
    exit(1)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if DISCORD_BOT_TOKEN == None:
    log.critical("No DISCORD_BOT_TOKEN environment variable is set.  Aborting...")
    exit(1)

TARGET_TIMEZONE = os.getenv("TARGET_TIMEZONE")
if TARGET_TIMEZONE == None:
    log.critical("No TARGET_TIMEZONE environment variable is set.  Aborting...")
    exit(1)

time_format = "%I:%M%p"

def linkToMarkdown(url = "", text = ""):
    return "[" + text + "](" + url + ")" 

def isOneDay(event):
    one_day = timedelta(days=1)

    if event.duration == one_day:
        return True

    return False

def endsToday(event):
    end = event.end.date()
    today = datetime.today().date()
    if end == today:
        return True
    
    else:
        return False

def hasEnded(event):
    end = localizeTime(event.end)
    now = localizeTime(datetime.now())
    if now > end:
        return True
    
    else:
        return False

def getRandomQuote():
    with open("quotes.json") as quotes_file:
            quotes = json.load(quotes_file)
            total = int(len(quotes))
            today_day = int(date.today().strftime("%d"))
            random_int = random.randint(0, total)
            pick_one = random_int
            author = quotes[pick_one]['author']
            if author == None:
                author = "Anonymous"
            message = str(quotes[pick_one]['text']) + " \n - _" + str(author + "_")
            return message

def localizeTime(orig):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(TARGET_TIMEZONE)
    utc = orig.replace(tzinfo=from_zone)
    target = utc.astimezone(to_zone)
    return target

def msgNoEvents():
    title = ""
    message = getRandomQuote()
    embedVar = discord.Embed(description=message)

client = discord.Client()

@client.event
async def on_ready():
    log.info(f'{client.user} has connected to Discord!')
    log.info("Getting guild w/ ID " + str(DISCORD_GUILD_ID))
    guild = client.get_guild(DISCORD_GUILD_ID)
    log.info("Got guild.")
    log.info("Getting channel w/ ID " + str(DISCORD_CHANNEL_ID))
    channel = guild.get_channel(DISCORD_CHANNEL_ID)

    ics_file = requests.get(ICAL_URL).text
    c = Calendar(ics_file)

    todayEvents = 0
    message = ""
    addedEvents = 0

    for e in c.timeline.today():
        todayEvents = todayEvents + 1
        if todayEvents > 0:
            break
    
    if todayEvents == 0:
        message = getRandomQuote()

    else:
        today = datetime.today()
        day_start_localized = localizeTime(today).replace(minute=0,hour=0,second=0)
        day_end_localized = localizeTime(today).replace(minute=59,hour=23,second=59)
        for event in c.timeline.included(day_start_localized, day_end_localized):
            print(str(event))
            addEvent = True

            if event.name == "":
                addEvent = False

            if event.all_day and isOneDay(event) and endsToday(event):
                addEvent = False

            if hasEnded(event):
                addEvent = False

            if addEvent:
                eventMsg = event.name

                if not event.all_day:
                    startTime = localizeTime(event.begin).strftime(time_format).lstrip("0").replace(" 0", " ")
                    endTime = localizeTime(event.end).strftime(time_format).lstrip("0").replace(" 0", " ")
                    eventMsg = eventMsg + " (" + str(startTime) + " - " + str(endTime) + ")"
                
                if event.location is not None and event.location != "":
                    eventMsg = eventMsg + " @ " + linkToMarkdown(url="https://maps.google.com?q=" + urllib.parse.quote_plus(event.location), text=str(event.location))
                    
                message = message + "\n" + "• " + eventMsg
                addedEvents = addedEvents + 1
        
        if addedEvents > 0:
            title = "\U0001f389 **Today's Events!** \U0001f389 \n"
            message = title + message + "\n\n" + getRandomQuote()
        else:
            message = getRandomQuote()

    
    embedVar = discord.Embed(description=message)
    log.info(str(message))
    await channel.send(embed=embedVar)

    log.info("Disconnecting")
    await client.close()
    
    return None

def lambda_handler(event, lambda_context):
    log.info("LAMBDA INVOKED! " + str(event) + " " + str(lambda_context))
    main()
    
    return None

def main():
    client.run(DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    main()
