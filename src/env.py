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
DISCORD_ADMIN_ID = os.environ["DISCORD_ADMIN_ID"]
DISCORD_INVITE_LINK = os.environ["DISCORD_INVITE_LINK"]

""" Absolute file paths """
ENV_PY = Path(__file__)
SRC_DIR = ENV_PY.parent
TEST_DIR = os.path.join(SRC_DIR.parent, "tests")
LOG_FILE = os.path.join(SRC_DIR, f"logs/bot.log")