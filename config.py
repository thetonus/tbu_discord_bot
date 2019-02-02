""" Load .env file variabless """
import os
import sentry_sdk

from orator import DatabaseManager, Model, Schema
from dotenv import load_dotenv, find_dotenv


# Load Environment
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Sentry Information
SENTRY_CLIENT_KEY = os.getenv("SENTRY_CLIENT_KEY")
sentry = sentry_sdk.init(SENTRY_CLIENT_KEY)

# Discord Information
DISCORD = {
    "NEWS_COMICS": {
        "WEBHOOK": os.getenv("NEWS_COMICS_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/comic/comic-news/feed",
        "TABLE": "comicNews",
    },
    "NEWS_MOVIE": {
        "WEBHOOK": os.getenv("NEWS_MOVIE_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/movie/movie-news/feed",
        "TABLE": "movieNews",
    },
    "NEWS_TV": {
        "WEBHOOK": os.getenv("NEWS_TV_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/tv/tv-news/feed",
        "TABLE": "tvNews",
    },
    "NEWS_VIDEOGAMES": {
        "WEBHOOK": os.getenv("NEWS_VIDEOGAMES_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/videogame/videogame-news/feed",
        "TABLE": "gamesNews",
    },
    "NEWS_MERCH": {
        "WEBHOOK": os.getenv("NEWS_MERCH_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/merchandise/merchandise-news/feed",
        "TABLE": "merchNews",
    },
    "NEWS_GENERAL": {
        "WEBHOOK": os.getenv("NEWS_GENERAL_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/general/general-news/feed",
        "TABLE": "generalNews",
    },
    "PODCAST_COMICS": {
        "WEBHOOK": os.getenv("PODCAST_COMICS_WEBHOOK"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/tbucp/feed",
        "TABLE": "comicsPodcast",
    },
    "BAT_BOOKS": {
        "WEBHOOK": os.getenv("BAT_BOOKS"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/tbu-bbfb/feed",
        "TABLE": "batBooks",
    },
    "BATGIRL_TO_ORACLE": {
        "WEBHOOK": os.getenv("BATGIRL_TO_ORACLE"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/bto/feed",
        "TABLE": "batgirlOracle",
    },
    "ROBIN_LOVES": {
        "WEBHOOK": os.getenv("ROBIN_LOVES"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/reltdp/feed",
        "TABLE": "robinLoves",
    },
    "BAT_FANS": {
        "WEBHOOK": os.getenv("BAT_FANS"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/tbu-batfans/feed",
        "TABLE": "batFans",
    },
    "YOUNG_JUSTICE": {
        "WEBHOOK": os.getenv("YOUNG_JUSTICE"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/elyj/feed",
        "TABLE": "youngJustice",
    },
    "GOTHAM_CHRONICLE": {
        "WEBHOOK": os.getenv("GOTHAM_CHRONICLE"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/tgc/feed",
        "TABLE": "gothamChronicle",
    },
    "TBU_COMMENTARIES": {
        "WEBHOOK": os.getenv("TBU_COMMENTARIES"),
        "FEED": "http://thebatmanuniverse.net/category/podcast/tbuc/feed",
        "TABLE": "tbuCommentaries",
    },
}

# Database information
DATABASE = {
    "default": {
        "driver": os.getenv("DB_DRIVER"),
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
}

# Creates Base Orator Model
db = DatabaseManager(DATABASE)
schema = Schema(db)
