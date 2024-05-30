import logging
import os
from telegram.ext import Application

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# hide info from httpx & apscheduler.executors.default
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

from tzbot.config import Development as Config

API_KEY = Config.API_KEY
LANG = Config.LANG
REMOVE_TAG = Config.REMOVE_TAG
WORDS_TO_FORWARD = Config.WORDS_TO_FORWARD
TIME_TO_DELETE = Config.TIME_TO_DELETE

try:
    OWNER_ID = set(int(x) for x in Config.OWNER_ID)
except ValueError:
    raise Exception("Your OWNER_ID variable is not a valid integer.")

try:
    FROM_CHATS = set(int(x) for x in Config.FROM_CHATS)
except ValueError:
    raise Exception("Your FROM_CHATS list does not contain valid integers.")

try:
    TO_CHATS = set(int(x) for x in Config.TO_CHATS or [])
except ValueError:
    raise Exception("Your TO_CHATS list does not contain valid integers.")

try:
    GROUPS_TO_DELETE = set(int(x) for x in Config.GROUPS_TO_DELETE)
except ValueError:
    raise Exception("Your GROUPS_TO_DELETE list does not contain valid integers.")

try:
    APPROVED_MEMBERS = set(int(x) for x in Config.APPROVED_MEMBERS)
except ValueError:
    raise Exception("Your APPROVED_MEMBERS list does not contain valid integers.")

try:
    GROUPS_TO_BAN = set(int(x) for x in Config.GROUPS_TO_BAN)
except ValueError:
    raise Exception("Your GROUPS_TO_BAN list does not contain valid integers.")

OWNER_ID = list(OWNER_ID)
FROM_CHATS = list(FROM_CHATS)
TO_CHATS = list(TO_CHATS)
GROUPS_TO_DELETE = list(GROUPS_TO_DELETE)
APPROVED_MEMBERS = list(APPROVED_MEMBERS)
GROUPS_TO_BAN = list(GROUPS_TO_BAN)

application = Application.builder().token(API_KEY).concurrent_updates(True).build()