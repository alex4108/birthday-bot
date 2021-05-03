# Birthday Bot

This script fetches an ICS (Calendar) file, and sends a Discord message listing today's events.

It runs in production on AWS Lambda to minimize costs ;)

## Python Virtualenv

```
virtualenv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
```


## dotenv file

The .env file requires 5 params:

`ICAL_URL` is the HTTPS URL to the ICS file containing the calendar data
`DISCORD_CHANNEL_ID` is the channel ID where to make announcements
`DISCORD_GUILD_ID` is the guild ID where to make announcements
`DISCORD_BOT_TOKEN` is the discord bot token
`ENV` is the environment you're running in.  Set to `live` when running in a live context.


## Running locally

A simple `python3 birthday-bot.py` should get you off the ground, after you've defined the required parameters in the .env file.

## Build & Deploy (to lambda)

```
bash build.sh && bash deploy.sh
```