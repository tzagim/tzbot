if not __name__.endswith("default_config"):
    import sys

    print(
        "The README is there to be read. Extend this sample config to a config file, don't just rename and change "
        "values here. Doing that WILL backfire on you.\nBot quitting.",
        file=sys.stderr,
    )
    quit(1)


# Create a new config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    REMOVE_TAG = False

    # REQUIRED
#    API_KEY = "1234567890:Abcdef1234567890GHIJ"  # API key obtained from BotFather
#    OWNER_ID = "1234567890"  # If you dont know, run the bot and do /id in your private chat with the bot

    # FOR AUTOMATICALLY FORWARDING MESSAGES
#    FROM_CHATS = [-1001234567890]  # List of chat id's to forward messages from
#    TO_CHATS = [-1001234567890]  # List of chat id's to forward messages to
    
    # FOR DELELTE MESSAGES AFTER X MINUTS
    GROUPS_TO_DELETE = [-1001234567890] # List of chat id's to delete messages from
    TIME_TO_DELETE = 900 # 15 min in sec


    WORDS_TO_FORWARD = '(.*)'

    # Supported languages
    # en, he
#    LANG = 'en'

class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
