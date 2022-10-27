# Birthday Bot

[![Tests](https://github.com/alex4108/birthday-bot/actions/workflows/test.yml/badge.svg)](https://github.com/alex4108/birthday-bot/actions/workflows/test.yml)
[![Release](https://github.com/alex4108/birthday-bot/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/alex4108/birthday-bot/actions/workflows/release.yml)
[![GitHub forks](https://img.shields.io/github/forks/alex4108/birthday-bot)](https://github.com/alex4108/birthday-bot/network)
[![GitHub stars](https://img.shields.io/github/stars/alex4108/birthday-bot)](https://github.com/alex4108/birthday-bot/stargazers)
![GitHub contributors](https://img.shields.io/github/contributors/alex4108/birthday-bot)
[![GitHub license](https://img.shields.io/github/license/alex4108/birthday-bot)](https://github.com/alex4108/birthday-bot/blob/main/LICENSE)
![GitHub All Releases](https://img.shields.io/github/downloads/alex4108/birthday-bot/total)
![Docker Pulls](https://img.shields.io/docker/pulls/alex4108/birthday-bot)
[![Discord](https://img.shields.io/discord/742969076623605830)](https://discord.gg/FpDjFEQ)

![Supports amd64](https://img.shields.io/badge/arch-amd64-brightgreen)

[![Discord Support](https://user-images.githubusercontent.com/7796475/89976812-2628c080-dc2f-11ea-92a1-fe87b6a9cf92.jpg)](https://discord.gg/FpDjFEQ)

This script fetches an ICS (Calendar) file, and sends a Discord message listing today's events.

If no events are found for the current day, the bot will message a "random" motivational quote.  Thanks [type.fit](https://type.fit/api/quotes) for the list!

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

_This project is no longer deployed via Lambda.  I now use a kubernetes cluster for all my deployments._

```
bash build.sh && bash deploy.sh
```

## Build & Deploy (to kubernetes)

See `.github/workflows/test.yml` for an idea of what it takes to build & deploy to Kubernetes.

#### Sample secret definition

```
kubectl create secret generic -n birthday-bot-test birthday-bot \
  --from-literal=discord_token=XX \
  --from-literal=discord_guild_id=XX \
  --from-literal=discord_channel_id=XX \
  --from-literal=ical_url=XX \
  --from-literal=timezone=XX
```