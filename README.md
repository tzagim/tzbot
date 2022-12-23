# tzbot

# Deleting join and leave messages

The bot must be granted deletion privileges in order to delete messages user leave or join the group.

# Auto Forwarder

A simple Telegram Python bot running on Python3 to automatically forward messages from one chat to another.


## Setting Up The Bot (Read Before Trying To Use!):
Please make sure to use the latest Python version. (*Recommended*)


### Configuration

There are two possible ways of configuring your bot: a `config.py` file, or ENV variables.

The prefered version is to use a `config.py` file, as it makes it easier to see all your settings grouped together.
This file should be placed in `tzbot` folder, alongside the `__main__.py` file . 
This is where your bot token will be loaded from, and most of your other settings.

It is recommended to import `default_config` and extend the `Config` class, as this will ensure your config contains all 
defaults set in the `default_config`, hence making it easier to upgrade.

An example `config.py` file could be:
```
from tzbot.default_config import Config


class Development(Config):
    API_KEY = "1234567890:Abcdef1234567890GHIJ"  # Your bot API key
    OWNER_ID = 1234567890  # Your user id

    # Make sure to include the '-' sign in group and channel ids.
    FROM_CHATS = [-1001234567890]  # List of chat id's to forward messages from.
    TO_CHATS = [-1001234567890, -1234567890]  # List of chat id's to forward messages to.
    
    # If you don't want to filter text with specific words to be forwarded, just delete the next line
    WORDS_TO_FORWARD = '(regex.*)(Some|text|to|filter)'

    REMOVE_TAG = True
    WORKERS = 4
```

If you can't have a `config.py` file (EG on Heroku), it is also possible to use environment variables.
The following environment variables are supported:

 - `ENV`: Setting this to `ANYTHING` will enable environment variables.

 - `API_KEY`: Your bot API key, as a string.
 - `OWNER_ID`: An integer of consisting of your owner ID.

 - `FROM_CHATS`: **Space separated** list of chat ID's to forward messages from. Do not forget to include the 
minus (-) sign in the chat ID's of groups and channels. You can add ID's of users too, to forward their 
messages with the bot.
 - `TO_CHATS`: **Space separated** list of chat ID's to forward messages to. Do not forget to include the 
minus (-) sign in the chat ID's of groups and channels. You can add ID's of users too, to forward messages to them.
 - `REMOVE_TAG`: Wether remove the "Forwarded From ...." tag or not.

 - `WEBHOOK`: Setting this to `ANYTHING` will enable webhooks when in env mode messages.
 - `URL`: The URL your webhook should connect to (only needed for webhook mode).
 - `CERT_PATH`: Path to your webhook certificate.
 - `PORT`: Port to use for your webhooks.

 - `WORKERS`: Number of threads to use. 4 is the recommended (and default) amount, but your experience may vary.
 **NOTE:** You may need to use more workers if the number of messages to be forwarded are more. 
 But going crazy with more threads wont necessarily speed up your bot due to the way python asynchronous calls work.


### Python dependencies

Install the necessary python dependencies by moving to the project directory and running:

`pip3 install -r requirements.txt`.

This will install all necessary python packages.


### Launch in Docker container

#### Requrements
 - Docker
 - docker-compose

Before launch you need to copy file ```env_dist``` to file ```.env``` and fill the values in it.

Then, simple run the command: ```docker-compose up -d```

You can view the logs by the command: ```docker-compose logs -f```

## Starting The Bot

Once you've setup your database and your configuration (see below) is complete, simply run:

`python3 -m tzbot`

### Credits

* [saksham2410](https://github.com/saksham2410) - AutoForwarder-TelegramBot
* [MrMissx](https://github.com/MrMissx) - Telegram_Forwarde
