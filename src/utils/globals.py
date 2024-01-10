"""
Accesses all required environment variables from the .env file
Also creates absolute paths for all important directories and folders
"""

from dotenv import load_dotenv
import os
from pathlib import Path

""" Env variables """
load_dotenv()
DEBUG = os.environ.get("DEBUG", "False")
BOT_TOKEN = os.environ["DISCORD_GYM_BOT_TOKEN"]
BOT_TEST_TOKEN = os.environ["BOT_TEST_TOKEN"]
BOT_TEST2_TOKEN = os.environ["BOT_TEST2_TOKEN"]
DISCORD_ADMIN_ID = os.environ["DISCORD_ADMIN_ID"]
DISCORD_INVITE_LINK = os.environ["DISCORD_INVITE_LINK"]

""" Absolute file paths """
ENV_PY_PATH = Path(__file__)
SRC_DIR_PATH = ENV_PY_PATH.parent.parent
LOG_FILE_PATH = os.path.join(SRC_DIR_PATH, f"logs/bot.log")
DB_PATH = os.path.join(SRC_DIR_PATH, "database/bot.db")
COGS_PATH = os.path.join(SRC_DIR_PATH, "cogs")
TEST_DIR_PATH = os.path.join(SRC_DIR_PATH.parent, "tests")
TEST_COGS_PATH = os.path.join(TEST_DIR_PATH, "cogs")

""" Bot """
BOT_PREFIX = "jim/"

""" Other """
TZ_LIST_URL = "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"