""" TBU Discord Bot  """
import feedparser
from typing import Tuple, List, Dict
from helpers.sentry import client

# User imports
from settings import DISCORD, db
from discord import discord_api


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

    result = db.table(table).where("title", article_title).where("link", article_url).where("published", article_date).get().serialize()
    if result:
        return False
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
            posts.append(article['link'])
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
    return hook.post()


def run(log) -> None:
    '''This function starts the Discord Bot. It allows the user to control the runtime enviroment settings.

    Arguments:
        webhooks {Dict} -- [This is a dictionary of all the Discord webhooks for the server.]
        log {[logger]} -- [Python logger]

    Returns:
        None
    '''

    # All the Discord Channels that I care about
    channels = set([
        "NEWS_COMICS",
        "NEWS_MOVIE",
        "NEWS_TV",
        "NEWS_VIDEOGAMES",
        "NEWS_MERCH",
        "NEWS_GENERAL",
        "PODCAST_COMICS",
    ])

    try:
        for channel in channels:
            log.info(f'Seeing if {channel} needs to be updated.')
            posts = read_article_feed(DISCORD[channel]["TABLE"].lower(), DISCORD[channel]["FEED"])
            if len(posts) > 0:
                log.info(f'{channel} needs to be updated.')
                # Sends all new posts from older to newer.
                posts = posts[::-1]
                for post in posts:
                    send(DISCORD[channel]["WEBHOOK"], post)
            else:
                log.info('No new posts')

    except Exception as err:
        log.critical(err)
        client.capture_exception()
