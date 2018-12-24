""" The Batman Universe news Discord Bot. """
import logging
from logging.config import fileConfig

# User Imports
from discord import bot
from helpers.sentry import client

# Initiate Logger
fileConfig('logging.ini')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    """ Discord Bot """
    try:
        # Discord Bot
        logger.info('Discord Bot Starting up')
        bot.run()
        logger.info('Discord Bot Finished')

    except Exception as err:
        logger.exception(err)
        client.capture_exception()
