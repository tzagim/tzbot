from telegram.ext import CallbackContext, MessageHandler, Filters
from telegram.update import Update
from tzbot import dispatcher

def joinleft(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    message_id = update.effective_message.message_id
    context.bot.delete_message(chat_id, message_id)

dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members | Filters.status_update.left_chat_member ,joinleft))
