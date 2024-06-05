from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters
from telegram.constants import ParseMode

from tzbot.strings import strings
from tzbot import bot, OWNER_ID, LANG

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user
    lang_code = LANG
    try:
        lang_code = message.from_user.language_code
    except (AttributeError, KeyError):
        pass
    if not (chat and message and user):
        return

    if chat.type == "private":
        if user.id in OWNER_ID:
            await message.reply_text(
            strings["pm_start"][lang_code].format(user.first_name, context.bot.first_name),
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.reply_text(strings["owner_only"][lang_code])
    else:
        await message.reply_text(strings["run_msg"][lang_code])

async def help(update: Update, _):
    chat = update.effective_chat
    message = update.effective_message
    lang_code = message.from_user.language_code
    if not (chat and message):
        return

    if not chat.type == "private":
        await message.reply_text(strings["pm_me"][lang_code])
    else:
        await message.reply_text(strings["pm_help"][lang_code])

bot.add_handler(CommandHandler("start", start))
bot.add_handler(CommandHandler("help", help, filters=filters.User(OWNER_ID)))
