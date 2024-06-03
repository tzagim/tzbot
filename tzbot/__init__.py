import logging
import json
from os import getenv, path

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, Defaults
from telegram import Update

# Load config.env
load_dotenv("config.env")

# Enable logging
logging.basicConfig(
    format='[ %(asctime)s: %(levelname)-2s ] %(name)-2s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('tzbot/log.txt', mode='a'), logging.StreamHandler()]
)

LOGGER = logging.getLogger(__name__)

# Hide info from httpx & apscheduler.executors.default
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

# Load json file
config_name = "chat_list.json"
if not path.isfile(config_name):
    LOGGER.error("No chat_list.json config file found! Exiting...")
    exit(1)
with open(config_name, "r") as data:
    CONFIG = json.load(data)

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    LOGGER.error("No BOT_TOKEN token provided!")
    exit(1)

try:
    OWNER_ID = set(int(x) for x in getenv("OWNER_ID", "0").split(","))
except ValueError:
    raise Exception("Your OWNER_ID list does not contain valid integers.")

OWNER_ID = list(OWNER_ID)

REMOVE_TAG = getenv("REMOVE_TAG", "False") in {"true", "True", 1}

try:
    GROUPS_TO_DELETE = set(int(x) for x in getenv("GROUPS_TO_DELETE", "0").split(","))
except ValueError:
    raise Exception("Your GROUPS_TO_DELETE list does not contain valid integers.")

GROUPS_TO_DELETE = list(GROUPS_TO_DELETE)
TIME_TO_DELETE = int(getenv("TIME_TO_DELETE", "0"))

LANG = str(getenv("DEFAULT_LANG"))
if not LANG:
    LANG = "en"

bf = Defaults(block=False)
bot = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).defaults(bf).build()
