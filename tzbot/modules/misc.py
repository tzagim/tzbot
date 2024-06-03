from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler, ContextTypes
from tzbot.strings import strings
from tzbot import bot, OWNER_ID, LANG

async def get_id(update: Update, _):
    message = update.effective_message
    chat = update.effective_chat
    try:
        lang_code = message.from_user.language_code
    except AttributeError or KeyError:
        lang_code = LANG

    if chat.type == 'private':  # Private chat with the bot
        return await message.reply_text(strings["your_id"][lang_code].format(chat.id), parse_mode=ParseMode.MARKDOWN)

    result = strings["chat_id"][lang_code].format(chat.id)
    if chat.is_forum:
        result += strings["forum_id"][lang_code].format(message.message_thread_id)

    if message.reply_to_message:
        forwarder = message.reply_to_message.from_user
        if message.reply_to_message.forward_from:  # Forwarded user
            sender = message.reply_to_message.forward_from
            result += strings["original_sender"][lang_code].format(sender.first_name, sender.id)
            result += strings["forwarder_user"][lang_code].format(forwarder.first_name if forwarder else 'Unknown', forwarder.id if forwarder else 'Unknown')

        if message.reply_to_message.forward_from_chat:  # Forwarded channel
            channel = message.reply_to_message.forward_from_chat
            result += strings["forwarder_channel"][lang_code].format(channel.title, channel.id)
            result += strings["forwarder_user"][lang_code].format(forwarder.first_name if forwarder else 'Unknown', forwarder.id if forwarder else 'Unknown')

    return await message.reply_text(
        result,
        parse_mode=ParseMode.MARKDOWN,
    )

GET_ID_HANDLER = MessageHandler(
    filters.COMMAND
    & filters.Regex(r"^/id")
    & (filters.User(OWNER_ID) | filters.ChatType.CHANNEL),
    get_id,
)

bot.add_handler(GET_ID_HANDLER)
