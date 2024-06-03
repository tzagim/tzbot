import importlib

from tzbot import LOGGER, bot
from tzbot.modules import ALL_MODULES

for module in ALL_MODULES:
    importlib.import_module("tzbot.modules." + module)

def run():
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    LOGGER.info("Starting bot...")
    bot.run_polling()
