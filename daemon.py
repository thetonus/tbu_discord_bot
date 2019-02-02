""" The Batman Universe news Discord Bot. """
import json
import logging
import logging.config
import os

# User Imports
from discord import bot


def setup_logging(
    default_path="configs/logging.json", default_level=logging.INFO, env_key="LOG_CFG"
):
    """ Setup logging configuration """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


# Initiate Logger
setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    """ Discord Bot """

    logger.info("Discord Bot Starting up")
    bot.run()
    logger.info("Discord Bot Finished")
