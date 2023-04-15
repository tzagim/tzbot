import importlib

from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, MessageHandler, filters

from tzbot import (API_KEY, LOGGER, OWNER_ID, LANG, application)
from tzbot.modules import ALL_MODULES

from tzbot.langdict import en, he

# Choose language
if LANG == 'he':
  LANG = he
else:
  LANG = en

PM_START_TEXT = LANG.get('Pm_Start')
PM_HELP_TEXT = LANG.get('Pm_Help')

# Adding modules
for module in ALL_MODULES:
    importlib.import_module("tzbot.modules." + module)

# Start
async def start(update, _):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    # Checking if this is a private chat 
    if chat.type == "private":
        await message.reply_text(
            PM_START_TEXT.format(user.first_name, application.bot.first_name),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply_text(LANG.get('Run'))


async def help(update, _):
    chat = update.effective_chat
    message = update.effective_message

    # Checking if this is a private chat
    if not chat.type == "private":
        await message.reply_text(LANG.get('Pm_Me'))
    else:
        await message.reply_text(PM_HELP_TEXT)

# Define error
async def error(update, context):
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)

def main():    
    # Commands
    start_handler = CommandHandler("start", start, filters=filters.User(OWNER_ID))
    help_handler = CommandHandler("help", help, filters=filters.User(OWNER_ID))

    application.add_handler(start_handler)
    application.add_handler(help_handler)

    LOGGER.info("Using long polling.")
    application.add_error_handler(error)
    application.run_polling()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()