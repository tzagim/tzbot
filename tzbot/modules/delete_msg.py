from telegram.error import BadRequest
from telegram.ext import MessageHandler, filters
from tzbot import bot, LOGGER, DELETE_AFTER

# create a dictionary to store messages
messages = {}
GROUP_IDS = list(DELETE_AFTER.keys())

LOGGER.debug(f"Auto-delete mapping loaded: {DELETE_AFTER}")


async def store_message(update, context):
    chat_id    = update.effective_chat.id
    message_id = update.effective_message.message_id

    delete_after = DELETE_AFTER.get(chat_id)
    if delete_after and delete_after > 0:
        context.job_queue.run_once(
            delete_message,
            delete_after,
            data=(chat_id, message_id)
        )

async def delete_message(context):
    chat_id, message_id = context.job.data
    try:
        # delete the message from the chat
        await context.bot.delete_message(chat_id, message_id)

    except BadRequest as err:
        if err.message == 'Message to delete not found':
            pass
        else:
            LOGGER.warning(f'Error deleting message: {err}')
    except Exception as err:
        LOGGER.warning(f'Error deleting message: {err}')
    else:
        # delete the message from the dictionary
        messages.pop((chat_id, message_id), None)

try:
    DELETE_MESSAGES = MessageHandler(
        filters.Chat(GROUP_IDS)
        & ~(filters.StatusUpdate.NEW_CHAT_MEMBERS
            | filters.StatusUpdate.LEFT_CHAT_MEMBER
            | filters.Regex(r"^/id|help|start")),
        store_message,
    )

    bot.add_handler(DELETE_MESSAGES, group=1)

except ValueError: 
    LOGGER.warning("I can't DELETE_MESSAGES, BOT must be made an administrator with delete message permission.")
