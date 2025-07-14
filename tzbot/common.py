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

def get_lang_code(message):
    if not message:
        return LANG
    try:
        return message.from_user.language_code
    except (AttributeError, KeyError):
        return LANG

def is_owner(user_id):
    return user_id in OWNER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat      = update.effective_chat
    message   = update.effective_message
    user      = update.effective_user
    lang_code = get_lang_code(update.effective_message)

    if not (chat and message and user):
        return

    if is_owner(user.id):
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
    lang_code = get_lang_code(update.effective_message)
    
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
    lang_code = get_lang_code(update.effective_message)

    if not (chat and message):
        return

    result = ''

    if chat.is_forum:
        result += strings['forum_id'][lang_code].format(message.message_thread_id)

    if message.reply_to_message:
        forward_origin = message.reply_to_message.forward_origin

        if forward_origin:
            forwarder = message.reply_to_message.from_user

            # Forwarded user
            if forward_origin.type == 'user':
                sender = forward_origin.sender_user

                # Check if the user is checking themselves
                if chat.id == sender.id:
                    result = ''
                else:
                    result += strings["original_sender"][lang_code].format(sender.first_name, sender.id)

            # Forwarded channel
            elif forward_origin.type == 'channel':
                channel = forward_origin.chat
                result += strings["original_channel"][lang_code].format(channel.title, channel.id)

            result += strings['forwarder_user'][lang_code].format(forwarder.first_name if forwarder else 'Unknown', forwarder.id if forwarder else 'Unknown')

    else:
        # Private chat with the bot
        if chat.type == 'private':
            result += strings['your_id'][lang_code].format(chat.id)
        else:
            result += strings['chat_id'][lang_code].format(chat.id)

    # Check if result is empty
    if not result:
        result = strings["empty_result"][lang_code]

    sent = await message.reply_text(result, parse_mode=ParseMode.MARKDOWN)

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
        filters = filters.User(OWNER_ID)
    ),
    group=0
)

bot.add_handler(
    CommandHandler(
        "id",
        id_cmd,
        filters = (filters.User(OWNER_ID) | filters.ChatType.CHANNEL)
    ),
    group=0
)
