from telegram.ext import MessageHandler, filters
from tzbot import bot, LOGGER, DELETE_AFTER
from tzbot.common import schedule_delete

GROUP_IDS = list(DELETE_AFTER.keys())

async def store_message(update, context):
    chat_id    = update.effective_chat.id
    message_id = update.effective_message.message_id
    schedule_delete(context, chat_id, message_id)

if GROUP_IDS:
    LOGGER.debug(f"Auto-delete mapping loaded: {DELETE_AFTER}")
    DELETE_MESSAGES = MessageHandler(
        filters.Chat(GROUP_IDS)
        & ~(filters.StatusUpdate.NEW_CHAT_MEMBERS
            | filters.StatusUpdate.LEFT_CHAT_MEMBER
        ),
        store_message,
    )
    bot.add_handler(DELETE_MESSAGES, group=1)
else:
    LOGGER.info("No chats configured for auto-delete (DELETE_AFTER is empty)")
