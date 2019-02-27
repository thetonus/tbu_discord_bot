""" Setup DB for Discord Bot"""
import json
import os
import json
import logging
import logging.config

from config import DISCORD, schema


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


def create(table: str):
    """ Initialize Database """
    logger.info(f"Creating table {table}")
    with schema.create(table) as table:
        table.string("title")
        table.string("link")
        table.string("published")
    logger.info(f"Table {table} created")


def delete(table: str):
    """ Cleanse Database """
    logger.info(f"Dropping table {table}")
    schema.drop(table)
    logger.info(f"Table {table} dropped")


if __name__ == "__main__":
    # All the Discord Channels that I care about
    ROOT_DIR = os.getcwd()  # This is your Project Root
    with open(os.path.join(ROOT_DIR, "configs", "channels.json")) as f:
        data = f.read()
        channels = json.loads(data)

    # Initialize
    # for channel in channels["channels"]:
    #     create(DISCORD[channel]["TABLE"])

    # Cleanse
    # for channel in channels["channels"]:
    #     delete(DISCORD[channel]["TABLE"])
