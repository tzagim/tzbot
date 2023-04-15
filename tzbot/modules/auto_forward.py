from typing import Union

from telegram import Message, MessageId
from telegram.ext import CallbackContext, filters, MessageHandler
from telegram.error import ChatMigrated

from tzbot import FROM_CHATS, LOGGER, REMOVE_TAG, TO_CHATS, WORDS_TO_FORWARD, application


async def send_message(message: Message, chat_id: int) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return await message.copy(chat_id)
    return await message.forward(chat_id)

async def forward(update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat:
        return
    from_chat_name = chat.title or chat.first_name or "Unknown chat"

    for chat in TO_CHATS:
        to_chat = await context.bot.get_chat(chat)
        to_chat_name = to_chat.title or to_chat.first_name or "Unknown chat"

        try:
            await send_message(message, chat)
        except ChatMigrated as err:
            await send_message(message, err.new_chat_id)
            LOGGER.warning(f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!")
        except:
            LOGGER.exception(f'Error while forwarding message from chat {from_chat_name} to chat {to_chat_name}.')

try:
    FORWARD_HANDLER = MessageHandler(
        filters.Chat(FROM_CHATS)
        & (~ filters.StatusUpdate.ALL)
        & (~ filters.COMMAND)
        & filters.Regex(WORDS_TO_FORWARD),
        forward,
    )

    application.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")
