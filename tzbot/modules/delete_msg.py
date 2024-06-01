from telegram.error import BadRequest
from telegram.ext import MessageHandler, filters
from tzbot import TIME_TO_DELETE, GROUPS_TO_DELETE, bot, LOGGER

# create a dictionary to store messages
messages = {}

async def store_message(update, context):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    message_text = update.effective_message.text

    # store the message in the dictionary
    messages[(chat_id, message_id)] = message_text

    # schedule a job to delete the message after X minutes
    context.job_queue.run_once(
        delete_message, TIME_TO_DELETE, data=(chat_id, message_id)
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
        filters.Chat(GROUPS_TO_DELETE) & ~(filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER | filters.Regex(r"^/id|help|start")),
        store_message,
    )

    bot.add_handler(DELETE_MESSAGES)

except ValueError: 
    LOGGER.warning("I can't DELETE_MESSAGES, BOT must be made an administrator with delete message permission.")