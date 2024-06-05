from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, MessageHandler, ContextTypes
from tzbot.strings import strings
from tzbot import bot, OWNER_ID, LANG

async def get_id(update: Update, _):
    message = update.effective_message
    chat = update.effective_chat
    lang_code = LANG
    try:
        lang_code = message.from_user.language_code
    except (AttributeError, KeyError):
        pass

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

    return await message.reply_text(
        result,
        parse_mode=ParseMode.MARKDOWN,
    )

GET_ID_HANDLER = MessageHandler(
    filters.COMMAND
    & filters.Regex(r'^/id')
    & (filters.User(OWNER_ID) | filters.ChatType.CHANNEL),
    get_id,
)

bot.add_handler(GET_ID_HANDLER)
