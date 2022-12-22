from telegram.ext import CallbackContext
from telegram.update import Update
from telegram.ext import MessageHandler, Filters
from tzbot import dispatcher, updater

def joinleft(update: Update, context: CallbackContext):
    context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)

def massagedel():
    updater.start_polling()
    ud = updater.dispatcher
    ud.add_handler(MessageHandler(Filters.status_update.new_chat_members | Filters.status_update.left_chat_member ,joinleft))

massagedel()
