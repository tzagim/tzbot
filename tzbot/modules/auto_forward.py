import asyncio
from typing import Union, Optional

from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated, RetryAfter
from telegram.ext import MessageHandler, filters, ContextTypes

from tzbot import bot, REMOVE_TAG, LOGGER
from tzbot.utils import get_destination, get_config, predicate_text

async def send_message(
    message: Message, chat_id: int, thread_id: Optional[int] = None
) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        msg = await message.copy(chat_id, message_thread_id=thread_id)
    else:
        msg = await message.forward(chat_id, message_thread_id=thread_id)
    
    LOGGER.debug(f"Sent message {msg.message_id} to chat {chat_id}")
    return msg

async def forwarder(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat

    if not message or not source:
        return

    dest = get_destination(source.id, message.message_thread_id)
    text = message.text or ""

    matched_destinations = []

    for config in dest:
        chat_id = config.destination[0].get_id() if config.destination else None

        LOGGER.debug(f"Checking filters for chat_id: {chat_id}")

        matches_filter = predicate_text(config.filters, text)
        matches_blacklist = predicate_text(config.blacklist, text)

        if matches_filter and not matches_blacklist:
            matched_destinations.append(config.destination)

    for destination in matched_destinations:
        for chat in destination:
            try:
                await send_message(message, chat.get_id(), chat.get_topic())
            except RetryAfter as err:
                LOGGER.warning(f"Rate limited, retrying in {err.retry_after} seconds")
                await asyncio.sleep(err.retry_after + 0.2)
                await send_message(message, chat.get_id(), thread_id=chat.get_topic())
            except ChatMigrated as err:
                await send_message(message, err.new_chat_id)
                LOGGER.warning(
                    f"Chat {chat.get_id()} has been migrated to {err.new_chat_id}. Update the config file!"
                )
            except Exception as err:
                LOGGER.error(f"Failed to forward message to {chat.get_id()} due to {err}")

FORWARD_HANDLER = MessageHandler(
    filters.Chat([config.source.get_id() for config in get_config() if config.destination])
    & ~filters.COMMAND
    & ~filters.StatusUpdate.ALL,
    forwarder,
)
bot.add_handler(FORWARD_HANDLER)
