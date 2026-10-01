from telegram.error import BadRequest
from telegram.ext import CallbackContext, MessageHandler, filters
from tzbot import bot, OWNER_ID, LOGGER

async def delete_message(update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    try:
        await context.bot.delete_message(chat_id, message_id)
    except BadRequest as err:
        if err.message == "Message can't be deleted":
            LOGGER.warning(
                f"Can't delete message in chat {chat_id}: the bot must be an administrator "
                "with delete messages permission."
            )
        elif err.message != "Message to delete not found":
            LOGGER.exception(f"Error while deleting message {message_id} in chat {chat_id}")

DELETE_JOIN = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS
    | filters.StatusUpdate.LEFT_CHAT_MEMBER
    | ~(filters.User(OWNER_ID) | filters.ChatType.CHANNEL | filters.ChatType.PRIVATE) & filters.Regex("^/"),
    delete_message,
)

bot.add_handler(DELETE_JOIN)
