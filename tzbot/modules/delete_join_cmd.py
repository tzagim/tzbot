from telegram.error import BadRequest
from telegram.ext import CallbackContext, MessageHandler, filters
from tzbot import bot, OWNER_ID

async def delete_message(update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    await context.bot.delete_message(chat_id, message_id)

try:
    DELETEֹ_JOIN = MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER | ~(filters.User(OWNER_ID) | filters.ChatType.CHANNEL) & filters.Regex("^/") ,delete_message,
    )

    bot.add_handler(DELETEֹ_JOIN)

except BadRequest as err:
    if err.message == "Message can't be deleted":
        LOGGER.exception("I can't DELETEֹ_JOIN because the BOT don't have permission, BOT must be made an administrator with delete message permission.")
    elif err.message != "Message to delete not found":
        LOGGER.exception("Error while purging chat messages.")