# Birthday Bot

The script simply needs to be invoked once every 24 hours.  Perhaps via Kubernetes or AWS Lambda + EventBridge

Anywho

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

