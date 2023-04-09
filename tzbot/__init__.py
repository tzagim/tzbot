import logging
import os

import telegram.ext as tg

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)


ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_KEY = os.environ.get("API_KEY", None)
    try:
        OWNER_ID = set(int(x) for x in os.environ.get("OWNER_ID", "").split())
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        FROM_CHATS = set(int(x) for x in os.environ.get("FROM_CHATS", "").split())
    except ValueError:
        raise Exception("Your FROM_CHATS list does not contain valid integers.")

    try:
        TO_CHATS = set(int(x) for x in os.environ.get("TO_CHATS", "").split())
    except ValueError:
        raise Exception("Your TO_CHATS list does not contain valid integers.")

    try:
        GROUPS_TO_DELELTE = set(int(x) for x in os.environ.get("GROUPS_TO_DELELTE", "").split())
    except ValueError:
        raise Exception("Your GROUPS_TO_DELELTE list does not contain valid integers.")

    REMOVE_TAG = bool(os.environ.get("REMOVE_TAG", False))
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    IP_ADDRESS = os.environ.get("IP_ADDRESS", "0.0.0.0")
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    WORKERS = int(os.environ.get("WORKERS", 4))
    WORDS_TO_FORWARD = str(os.environ.get("WORDS_TO_FORWARD"))
    TIME_TO_DELELTE = int(os.environ.get("TIME_TO_DELELTE", 10800))

else:
    from tzbot.config import Development as Config

    API_KEY = Config.API_KEY
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
        GROUPS_TO_DELELTE = set(int(x) for x in Config.GROUPS_TO_DELELTE)
    except ValueError:
        raise Exception("Your GROUPS_TO_DELELTE list does not contain valid integers.")

    LANG = Config.LANG

    REMOVE_TAG = Config.REMOVE_TAG
    WEBHOOK = Config.WEBHOOK
    IP_ADDRESS = Config.IP_ADDRESS
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    WORKERS = Config.WORKERS
    WORDS_TO_FORWARD = Config.WORDS_TO_FORWARD
    TIME_TO_DELELTE = Config.TIME_TO_DELELTE

updater = tg.Updater(API_KEY, workers=WORKERS, use_context=True)

dispatcher = updater.dispatcher

OWNER_ID = list(OWNER_ID)
FROM_CHATS = list(FROM_CHATS)
TO_CHATS = list(TO_CHATS)
GROUPS_TO_DELELTE = list(GROUPS_TO_DELELTE)
