import logging
import datetime

from bot import FamilyFundsBot
from bot.routing import HANDLERS
from constants import LOGGING_FORMAT, API_TOKEN, BOT_LOG_FILEPATH


logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, filename=BOT_LOG_FILEPATH)


def main() -> None:
    ffbot = FamilyFundsBot(API_TOKEN)
    ffbot.add_handlers(HANDLERS)
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.run_polling()


if __name__ == '__main__':
    main()