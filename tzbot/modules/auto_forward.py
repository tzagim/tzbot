import asyncio
from typing import Union, Optional

from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated, RetryAfter
from telegram.ext import MessageHandler, filters, ContextTypes

from tzbot import bot, REMOVE_TAG, LOGGER
from tzbot.common import schedule_delete
from tzbot.utils import get_destination, get_config, predicate_text

FORWARD_CHAT_IDS = [cfg.source.get_id() for cfg in get_config() if cfg.destination]


async def send_message(
    m: Message,
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    thread_id: Optional[int] = None,
) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        msg = await m.copy(chat_id, message_thread_id=thread_id)
    else:
        msg = await m.forward(chat_id, message_thread_id=thread_id)

    LOGGER.debug(f"Sent message {msg.message_id} to chat {chat_id}")

    if context:
        schedule_delete(context, chat_id, msg.message_id)
    return msg


async def forwarder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat

    if not message or not source:
        return

    dest_configs = get_destination(source.id, message.message_thread_id)
    text = message.text or message.caption or ""

    for cfg in dest_configs:
        if not (
            predicate_text(cfg.filters, text)
            and not predicate_text(cfg.blacklist, text)
        ):
            continue

        for dest in cfg.destination or []:
            cid = dest.get_id()
            tid = dest.get_topic()
            try:
                await send_message(message, cid, context, tid)
            except RetryAfter as err:
                LOGGER.warning(f"Rate limited, retrying in {err.retry_after} seconds")
                await asyncio.sleep(err.retry_after + 0.2)
                await send_message(message, cid, context, tid)
            except ChatMigrated as err:
                await send_message(message, err.new_chat_id, context, None)
                LOGGER.warning(
                    f"Chat {cid} has been migrated to {err.new_chat_id}. Update the config file!"
                )
            except Exception:
                LOGGER.error(f"Unexpected error forwarding to {cid}")


FORWARD_HANDLER = MessageHandler(
    filters.Chat(FORWARD_CHAT_IDS) & ~filters.COMMAND & ~filters.StatusUpdate.ALL,
    forwarder,
)
bot.add_handler(FORWARD_HANDLER, group=0)
