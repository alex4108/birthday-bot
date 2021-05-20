# Birthday Bot

[![Build Status](https://travis-ci.com/alex4108/birthday-bot.svg?branch=main)](https://travis-ci.com/alex4108/birthday-bot)

This script fetches an ICS (Calendar) file, and sends a Discord message listing today's events.

If no events are found for the current day, the bot will message a "random" motivational quote.  Thanks [type.fit](https://type.fit/api/quotes) for the list!

It runs in production on AWS Lambda to minimize costs ;)

This project was originally developed using Google Calendar.  The values of the ICS format may vary between calendar services.

## Python Virtualenv

```
virtualenv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
```

## dotenv file

The .env file requires 6 params:

`ICAL_URL` is the HTTPS URL to the ICS file containing the calendar data

`DISCORD_CHANNEL_ID` is the channel ID where to make announcements

`DISCORD_GUILD_ID` is the guild ID where to make announcements

`DISCORD_BOT_TOKEN` is the discord bot token

`ENV` is the environment you're running in.  Set to `live` when running in a live context.

`TARGET_TIMEZONE` is the target timezone you want to display messages in, eg `America/Chicago`

## Running locally

A simple `python3 birthday-bot.py` should get you off the ground, after you've defined the required parameters in the .env file.

## Build & Deploy (to lambda)

```
bash build.sh && bash deploy.sh
```