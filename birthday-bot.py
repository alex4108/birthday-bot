from ics import Calendar
from common import initLogger
from dotenv import load_dotenv, find_dotenv
import requests
import logging
import discord
import os
import asyncio

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



client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    log.info("Getting guild w/ ID " + str(DISCORD_GUILD_ID))
    guild = client.get_guild(DISCORD_GUILD_ID)
    log.info("Got guild.")
    log.info("Getting channel w/ ID " + str(DISCORD_CHANNEL_ID))
    channel = guild.get_channel(DISCORD_CHANNEL_ID)

    ics_file = requests.get(ICAL_URL).text
    c = Calendar(ics_file)
    for event in c.timeline.today():
        log.info("Got event: " + str(event.name))
        message = "Today is " + event.name
        await channel.send(message)


client.run(DISCORD_BOT_TOKEN)
