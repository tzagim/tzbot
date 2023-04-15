# tzbot
### *please note:*

version 2.x works with Telegram Python bot ver 20+

version 1.X works with Telegram Python bot ver 13.15 and below!!

# Deleting join and leave messages

The bot must be granted deletion privileges in order to delete messages user leave or join the group.

# Auto Forwarder

A simple Telegram Python bot running on Python3 to automatically forward messages from one chat to another.

# Auto Delete messages after X time
Automatic deletion of messages after a specified period of time, please note that you cannot delete messages of another bot, Because of Telegram limitations.

A simple Telegram Python bot running on Python3 to automatically forward messages from one chat to another.

## Setting Up The Bot (Read Before Trying To Use!):
Please make sure to use the latest Python version. (*Recommended*)


### Configuration

There are two possible ways of configuring your bot: a `config.py` file.

The prefered version is to use a `config.py` file, as it makes it easier to see all your settings grouped together.
This file should be placed in `tzbot` folder, alongside the `__main__.py` file . 
This is where your bot token will be loaded from, and most of your other settings.

It is recommended to import `default_config` and extend the `Config` class, as this will ensure your config contains all 
defaults set in the `default_config`, hence making it easier to upgrade.

#### *An action you don't want to perform, just ignore lines that run it.*

An example `config.py` file could be:
```
from tzbot.default_config import Config


class Development(Config):
    API_KEY = "1234567890:Abcdef1234567890GHIJ"  # Your bot API key
    OWNER_ID = [1234567890]  # List of your's id and your best freind :)

    # Make sure to include the '-' sign in group and channel ids.
    FROM_CHATS = [-1001234567890]  # List of chat id's to forward messages from.
    TO_CHATS = [-1001234567890, -1234567890]  # List of chat id's to forward messages to.
    
    # If you want to delete messages.
    GROUPS_TO_DELETE = [-1001234567890] # List of chat id's to delete messages from
    TIME_TO_DELETE = 900 # 15 min in sec, you can use also 15*60
    
    # If you don't want to filter text with specific words to be forwarded, use regex.
    WORDS_TO_FORWARD = '(regex.*)(Some|text|to|filter)'
    
    # You can communicate with the bot in supported languages (Hebrew and English, for now) the default is English.
    LANG = 'he' # If you want to use in Hebrew

    REMOVE_TAG = True
```

If you can't have a `config.py` file, it is also possible to use environment variables.
The following environment variables are supported:

 - `API_KEY`: Your bot API key, as a string.
 - `OWNER_ID`:  **Space separated** List of consisting of your owner ID's.

 - `FROM_CHATS`: **Space separated** list of chat ID's to forward messages from. Do not forget to include the 
minus (-) sign in the chat ID's of groups and channels. You can add ID's of users too, to forward their 
messages with the bot.
 - `TO_CHATS`: **Space separated** list of chat ID's to forward messages to. Do not forget to include the 
minus (-) sign in the chat ID's of groups and channels. You can add ID's of users too, to forward messages to them.
 - `REMOVE_TAG`: Wether remove the "Forwarded From ...." tag or not.

 - `GROUPS_TO_DELETE`: **Space separated** list of chat ID's to delete messages from after a time that you set in the next option. 
Do not forget to include the minus (-) sign in the chat ID's of groups and channels. You can add ID's of users too, to forward messages to them.
 - `TIME_TO_DELETE`: An integer of seconds to delete, can also be given through a mathematical exercise, for example 15*60 

 - `WORDS_TO_FORWARD`: If you don't want to filter text with specific words to be forwarded, use regex. 

 - `LANG`: The language in which the bot will answer you, Hebrew and English are currently supported, the default is English

### Python dependencies

Install the necessary python dependencies by moving to the project directory and running:

`pip3 install -r requirements.txt`.

This will install all necessary python packages.

## Starting The Bot

Once you've setup your database and your configuration (see below) is complete, simply run:

`python3 -m tzbot`

### Credits
For an early version of the bot: [MrMissx](https://github.com/MrMissx) - Telegram_Forwarder
