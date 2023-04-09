from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters
from telegram.ext.jobqueue import Job
from telegram.update import Update
from tzbot import dispatcher, TIME_TO_DELELTE, GROUPS_TO_DELELTE

# create a dictionary to store messages
messages = {}

def store_message(update, context):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    message_text = update.effective_message.text

    # store the message in the dictionary
    messages[(chat_id, message_id)] = message_text

    # schedule a job to delete the message after X minutes
    context.job_queue.run_once(delete_message, TIME_TO_DELELTE, context=(chat_id, message_id))

def delete_message(context):
    chat_id, message_id = context.job.context
    try:
       context.bot.delete_message(chat_id, message_id)
    except BadRequest as err:
        if err.message == "Message can't be deleted":
            LOGGER.exception("Cannot delete all messages. The messages may be too old, I might not have delete rights, or this might not be a supergroup.")
        elif err.message != "Message to delete not found":
            LOGGER.exception("Error while purging chat messages.")
    except:
        return

    # delete the message from the dictionary and from the chat
    messages.pop((chat_id, message_id), None)

dispatcher.add_handler(MessageHandler(Filters.chat(GROUPS_TO_DELELTE) & Filters.text, store_message))