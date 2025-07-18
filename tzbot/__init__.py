import logging
import json
from os import getenv, path
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, Defaults

# Load config.env
load_dotenv("config.env")

# Enable logging
logging.basicConfig(
    format='%(asctime)s: %(levelname)-2s - %(name)-2s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('tzbot/tzbot.log', mode='a'),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger(__name__)

# Hide info from httpx & apscheduler.executors.default & apscheduler
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

APSCHEDULER_LOG_LEVEL = getenv("APSCHEDULER_LOG_LEVEL", "INFO").upper()
logging.getLogger("apscheduler").setLevel(getattr(logging, APSCHEDULER_LOG_LEVEL, logging.INFO))

# Don't show info about added/removed jobs
try:
    APSCHEDULER_SCHEDULER_INFO = int(getenv("APSCHEDULER_SCHEDULER_INFO", 0))
except ValueError:
    APSCHEDULER_SCHEDULER_INFO = 0  

class APSchedulerFilter(logging.Filter):
    def __init__(self):
        self.filter_enabled = APSCHEDULER_SCHEDULER_INFO == 0

    def filter(self, record):
        if self.filter_enabled:
            return not ("Added job" in record.msg or "Removed job" in record.msg)
        return True

logging.getLogger("apscheduler.scheduler").addFilter(APSchedulerFilter())

# Load json file
try:
    with open("chat_list.json", encoding="utf-8") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    LOGGER.error("chat_list.json not found. Exiting.")
    exit(1)

# build delete-after mapping
DELETE_AFTER = {
    int(item["source"]): int(item["delete_after"])
    for item in CONFIG
    if "delete_after" in item
}
LOGGER.info(f"Auto-delete mapping loaded: {DELETE_AFTER}")

# core bot instance
BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    LOGGER.error("No BOT_TOKEN token provided!")
    exit(1)

# Owner ID
try:
    OWNER_ID = set(int(x) for x in getenv("OWNER_ID", "0").split(","))
except ValueError:
    raise Exception("Your OWNER_ID list does not contain valid integers.")

OWNER_ID = list(OWNER_ID)

# Remove tag option
REMOVE_TAG = getenv("REMOVE_TAG", "False") in {"true", "True", 1}

# Default language
LANG = str(getenv("DEFAULT_LANG"))
if not LANG:
    LANG = "en"

bf = Defaults(block=False)
bot = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .concurrent_updates(True)
    .defaults(bf)
    .build()
)

import tzbot.common
