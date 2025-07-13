from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, filters
from telegram.constants import ParseMode
from telegram.error import BadRequest

from tzbot.strings import strings
from tzbot import bot, OWNER_ID, LANG, LOGGER, DELETE_AFTER

GROUP_IDS = list(DELETE_AFTER.keys())

async def delete_job(context: ContextTypes.DEFAULT_TYPE):
    chat_id, message_id = context.job.data
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        LOGGER.debug(f"Deleted message {message_id} in chat {chat_id}")
    except BadRequest as err:
        if err.message != 'Message to delete not found':
            LOGGER.warning(f"Error deleting message {message_id}: {err}")

def schedule_delete(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    delay = DELETE_AFTER.get(chat_id)
    if delay and delay > 0:
        context.job_queue.run_once(
            delete_job,
            delay,
            data=(chat_id, message_id)
        )
        LOGGER.debug(
            f"Scheduled delete of message {message_id}"
            f" in chat {chat_id} after {delay}s"
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat      = update.effective_chat
    message   = update.effective_message
    user      = update.effective_user
    lang_code = LANG
    try:
        lang_code = message.from_user.language_code
    except (AttributeError, KeyError):
        pass

    if not (chat and message and user):
        return

    if user.id in OWNER_ID:
        if chat.type == "private":
            sent = await message.reply_text(
                strings["pm_start"][lang_code].format(
                    user.first_name, context.bot.first_name
                ),
                parse_mode=ParseMode.HTML,
            )
        else:
            sent = await message.reply_text(strings["run_msg"][lang_code])
    else:
        sent = await message.reply_text(strings["owner_only"][lang_code])
    
    if chat.id in DELETE_AFTER:
        schedule_delete(context, chat.id, message.message_id)
        schedule_delete(context, chat.id, sent.message_id)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat      = update.effective_chat
    message   = update.effective_message
    lang_code = message.from_user.language_code
    if not (chat and message):
        return

    if chat.type != "private":
        sent = await message.reply_text(strings["pm_me"][lang_code])
    else:
        sent = await message.reply_text(strings["pm_help"][lang_code])

    if chat.id in DELETE_AFTER:
        schedule_delete(context, chat.id, message.message_id)
        schedule_delete(context, chat.id, sent.message_id)

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat    = update.effective_chat
    message = update.effective_message
    if not (chat and message):
        return

    sent = await message.reply_text(f"Chat ID is: {chat.id}")

    if chat.id in DELETE_AFTER:
        schedule_delete(context, chat.id, message.message_id)
        schedule_delete(context, chat.id, sent.message_id)

bot.add_handler(
    CommandHandler(
        "start",
        start,
        filters = (filters.User(OWNER_ID) | filters.ChatType.PRIVATE)
    ),
    group=0
)

bot.add_handler(
    CommandHandler(
        "help",
        help,
        filters = filters.User(OWNER_ID)),
    group=0
)

bot.add_handler(
    CommandHandler("id", id_cmd),
    group=0
)
