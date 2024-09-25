# tzbot
### *please note:*
version 3.x works with Telegram Python bot ver 21+

version 2.x works with Telegram Python bot ver 20-21

version 1.X works with Telegram Python bot ver 13.15 and below!!

## Features
#### Deleting join and leave messages and commands

The bot must be granted deletion privileges in order to delete messages user leave or join the group, and also commands by users other than the bot owner.

#### Auto Forwarder

A simple Telegram Python bot running on Python3 to automatically forward messages from one chat to another.

#### Auto Delete messages after X time
Automatic deletion of messages after a specified period of time, please note that you cannot delete messages of another bot, Because of Telegram limitations.

#### Translation
Languages ​​can be added in `strings.py`, the default language is the user's language, if the user's language cannot be found or in channels the default is English.

## Setting Up The Bot (Read Before Trying To Use!):
Please make sure to use the latest Python version. (*Recommended*)

### Configuration

Configuring your bot: a `config.env` and `chat_list.json` files.

This file should be placed in `tzbot` folder, alongside the `__main__.py` file . 
This is where your bot token will be loaded from, and most of your other settings.

#### `config.env`

Template env may be found in `sample.config.env`. Rename it to `config.env` and fill in the values:

- `BOT_TOKEN` - Telegram bot token. You can get it from [@BotFather](https://t.me/BotFather)

- `OWNER_ID` - An integer or a comma-separated list of consisting of your owner ID.

- `REMOVE_TAG` - set to `True` if you want to remove the tag ("Forwarded from xxxxx") from the forwarded message.

- `GROUPS_TO_DELETE` = An integer or a comma-separated list of consisting of groups from which you want to delete messages after the set time.

- `TIME_TO_DELETE` = An integer to set time to delete in seconds.
 
- `DEFAULT_LANG` = Default language when the user language cannot be retrieved and in channels, if blank defaults to English.

#### `chat_list.json`

Template chat_list may be found in `chat_list.sample.json`. Rename it to `chat_list.json`.

This file contains the list of chats to forward messages from and to. The bot expect it to be an Array of objects with the following structure:

```json
[
  {
    "source": -10012345678,
    "destination": [-10011111111, "-10022222222#123456"]
  },
  {
    "source": "-10087654321#000000", // Topic/Forum group
    "destination": ["-10033333333#654321"],
    "filters": ["word1", "word2"] // message that contain this word will be forwarded
  },
  {
    "source": -10087654321,
    "destination": [-10033333333],
    "blacklist": ["word3", "word4"] // message that contain this word will not be forwarded
  },
  {
    "source": -10087654321,
    "destination": [-10033333333],
    "filters": ["word5"],
    "blacklist": ["word6"]
    // message must contain word5 and must not contain word6 to be forwarded
  }
]
```

An example `config.env` file could be:

```env
BOT_TOKEN = 1234567890:Abcdef1234567890GHIJ
OWNER_ID = 1234567890, 0987654321
REMOVE_TAG = True
GROUPS_TO_DELETE = -1001234567890, -1234567890
TIME_TO_DELETE = 900
DEFAULT_LANG = en
```
- `source` - The chat ID of the chat to forward messages from. It can be a group or a channel.

  > If the source chat is a Topic groups, you **MUST** explicitly specify the topic ID. The bot will ignore incoming message from topic group if the topic ID is not specified.

- `destination` - An array of chat IDs to forward messages to. It can be a group or a channel.

  > Destenation supports Topics chat. You can use `#topicID` string to forward to specific topic. Example: `[-10011111111, "-10022222222#123456"]`. With this config it will forward to chat `-10022222222` with topic `123456` and to chat `-10011111111` .

- `filters` (Optional) - An array of strings to filter words. If the message containes any of the strings in the array, it **WILL BE** forwarded.

- `blacklist` (Optional) - An array of strings to blacklist words. If the message containes any of the string in the array, it will **NOT BE** forwarded.

You may add as many objects as you want. The bot will forward messages from all the chats in the `source` field to all the chats in the `destination` field. Duplicates are allowed as it already handled by the bot.

Installing
==========


### Python dependencies
Install the necessary python dependencies by moving to the project directory and running:

```shell
$ git clone https://github.com/tzagim/tzbot
$ cd tzbot
```
If you are using pip:

```shell
$ pip install -r requirements.txt
```

If you are using advanced versions of linux that pip cannot be used:
```shell
$ sudo apt install python3-anyio python3-certifi python3-h11 python3-httpcore python3-httpx python3-idna python3-dotenv python3-python-telegram-bot python3-rfc3986 python3-sniffio python3-apscheduler
```

This will install all necessary python packages.

### Launch in Docker container

#### Requrements

- Docker
- docker compose

Before launch make sure all configuration are completed (`config.env` and `chat_list.json`)!

Then, simply run the command:

```shell
docker compose up -d
```

You can view the logs by the command:

```shell
docker compose logs -f
```


Starting The Bot
==========

Once you've setup your database and your configuration (see below) is complete, simply run:

    $ python3 -m tzbot

Can be run in a screen with the following command:

    $ screen -dmS tzbot python3 -m tzbot

### Credits
Based on: [MrMissx](https://github.com/MrMissx) - [Telegram_Forwarder](https://github.com/MrMissx/Telegram_Forwarder)
