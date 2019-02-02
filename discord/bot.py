""" TBU Discord Bot  """
import datetime
import json
import logging
import os
from typing import Dict, List, Tuple

import feedparser
import sentry_sdk

from config import DISCORD, db
from discord import discord_api

logger = logging.getLogger(__name__)


def article_is_not_db(table: str, article_title: str, article_url: str, article_date: str) -> bool:
    """ Check if a given pair of article title and date
    is in the database.
    Args:
        article_title (str): The title of an article
        article_url (str): The url of an article
        article_date  (str): The publication date of an article
    Return:
        True if the article is not in the database
        False if the article is already present in the database
    """

    result = db.table(table).where("title", article_title).where(
        "link", article_url).where("published", article_date).get().serialize()

    if result:
        logger.debug(
            f"Article '{article_title}' not found. Needs to be imported.")
        return False

    logger.debug(f"Article '{article_title}' found. Needs not be imported.")
    return True


def add_article_to_db(table: str, article_title: str, article_url: str, article_date: str) -> None:
    """ Add a new article title and date to the database
    Args:
        table (str): current table
        article_title (str): The title of an article
        article_url (str): The url of an article
        article_date (str): The publication date of an article
    """

    db.table(table).insert({
        'title': article_title,
        'link': article_url,
        'published': article_date,
    })
    logger.debug(f"Article '{article_title}' inserted")


def read_article_feed(table: str, FEED: str) -> List[str]:
    """ Get articles from RSS feed 

    Arguments:
        table {str} -- [DB table that needs to be updated]
        feed {str} -- [RSS feed]

    Returns:
        posts {list} -- List of new posts to send

    """

    posts = list()
    raw_feed = feedparser.parse(FEED)
    # Gets the lastest 20 feeds - if not it would download all posts.
    feed = raw_feed['entries'][0:20]
    for article in feed:
        if article_is_not_db(table, article['title'], article['link'], article['published']):
            posts.append(
                {'link': article['link'], 'published': article['published']})
            add_article_to_db(table,
                              article['title'],  article['link'], article['published'])
    return posts


def send(hook: str, msg: str) -> None:
    '''Post message into specific channel on the Discord Server.

    Arguments:
        webhool {str} -- [Webhook of Discord Server where you want to post the message]
        msg {str} -- [Post Content Body]

    Returns:
        None
    '''

    hook = discord_api.Webhook(hook, msg=msg)
    result, status = hook.post()

    if not result:
        sentry_sdk.capture_message(f"A {status} error occured.")

    return None


def run(debug=False) -> None:
    '''This function starts the Discord Bot. It allows the user to control the runtime enviroment settings.

    Arguments:
        webhooks {Dict} -- [This is a dictionary of all the Discord webhooks for the server.]
        log {[logger]} -- [Python logger]

    Returns:
        None
    '''

    # All the Discord Channels that I care about
    ROOT_DIR = os.getcwd()  # This is your Project Root
    with open(f'{ROOT_DIR}/configs/channels.json') as f:
        data = f.read()
        channels = json.loads(data)

    try:
        for channel in channels["channels"]:
            logger.info(f'Seeing if {channel} needs to be updated.')
            posts = read_article_feed(
                DISCORD[channel]["TABLE"], DISCORD[channel]["FEED"])
            if len(posts) > 0:
                logger.info(f'{channel} needs to be updated.')

                # Sends all new posts from older to newer.
                def convert(post):
                    """ Convert published date to datetime for comparison """
                    date_str = post["published"][:-6]
                    post["published"] = datetime.datetime.strptime(
                        date_str, '%a, %d %b %Y %H:%M:%S').date()
                    return post

                # Convert Post's date to datetime
                posts = [convert(post) for post in posts]

                # Sort posts based on oldest to newest
                posts = sorted(posts, key=lambda k: k['published'])

                for post in posts:
                    if not debug:
                        send(DISCORD[channel]["WEBHOOK"], post['link'])
                    else:
                        logger.info(f"Here is the post: {post['link']}")
            else:
                logger.info('No new posts')

    except Exception as err:
        logger.exception(err)
        sentry_sdk.capture_exception()
