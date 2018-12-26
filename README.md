# The Batman Universe Discord Bot

TBU uses Discord to talk about comics with their audience. I realized that the editor in chief spent a long time manually cutting and pasting the articles of the site into specific Discord channels.
Since TBU is a Wordpress site, I wondered if there would be a way to took at the rss feeds and add new stories to the Discord server. The "discord_bot" allows the autoposting of new TBU content when
it is published on the site.

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on how to deploy the project on a live system.

### Prerequisites

Here are the prerequisite modules used in this application.
```
orator
feedparser
sentry_sdk
python-dotenv
```

### Installing the conventional way


Install dependencies

```
pip3 install -r requirements.txt
```
In your `.env` file, enter your Sentry api key, your MySql Database credentials, and Discord webhook information. In config.py, change the rss feeds and database tables to yours.

## Start Application

Initiate daemon
```
python3 daemon.py
```

## Authors

* **[Tony Hammack](https://github.com/hammacktony/)**


## License

This project is licensed under the MIT License - see the 
[LICENSE.md](LICENSE.md) file for details
