import importlib
import traceback
from tzbot import LOGGER, bot
from tzbot.modules import ALL_MODULES
from telegram import Update
from telegram.ext import ContextTypes

# Import all modules
for module in ALL_MODULES:
    importlib.import_module("tzbot.modules." + module)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_type = context.error.__class__.__name__
    err_msg = str(context.error)

    if "httpx" in err_type or "NetworkError" in err_type:
        LOGGER.warning(f"Network issue: {err_type}: {err_msg}")
    else:
        LOGGER.error(f"Unexpected error: {err_type}: {err_msg}")
        LOGGER.debug("Full traceback:\n" + "".join(traceback.format_exception(None, context.error, context.error.__traceback__)))

def run():
    bot.add_error_handler(error_handler)
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    LOGGER.info("Starting bot...")
    bot.run_polling()
    LOGGER.info("Bot stopped cleanly.")
