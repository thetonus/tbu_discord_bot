""" The Batman Universe news Discord Bot. """
import logging
from logging.config import fileConfig

# User Imports
from discord import bot
from helpers.sentry import client


if __name__ == '__main__':
    try:
        # Initiate Logger
        fileConfig('logging.ini')
        log = logging.getLogger()

        # ------------ For process scheduler ------------

        # Discord Bot
        log.info('Discord Bot Starting up')
        bot.run(log)
        log.info('Discord Bot Finished')

    except Exception as e:
        log.critical(e)
        client.capture_exception()
