from telegram.ext import CallbackContext
from telegram.update import Update
from telegram.ext import MessageHandler, Filters
from tzbot import API_KEY, dispatcher, updater

def joinleft(update: Update, context: CallbackContext):
    context.bot.delete_message(chat_id=update.message.chat_id,message_id=update.message.message_id)

def massagedel():
    updater.start_polling()
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,joinleft))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,joinleft))

massagedel()