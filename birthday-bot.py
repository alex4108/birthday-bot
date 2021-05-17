from ics import Calendar
from common import initLogger
from dotenv import load_dotenv, find_dotenv
import requests
import logging
import discord
import os
import asyncio
import json
from datetime import date
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
    for e in c.timeline.today():
        todayEvents = todayEvents + 1
        if todayEvents > 0:
            break
    
    if todayEvents == 0:
        message = getRandomQuote()
        await channel.send(str(message))
    else:
        message =  "\U0001f389 **Today's Events!** \U0001f389 \n"
        for event in c.timeline.today():
            if event.name != "":
                message = message + "\n" + "• " + event.name
        print(str(message))
        message = message + "\n\n" + getRandomQuote()
        await channel.send(message)

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
