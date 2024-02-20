import logging
import datetime

import alembic.config

from bot import FamilyFundsBot
from bot.routing import HANDLERS
from constants import LOGGING_FORMAT, API_TOKEN, BOT_LOG_FILEPATH


logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, filename=BOT_LOG_FILEPATH)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    alembic.config.main(argv=['check'])
    ffbot = FamilyFundsBot(API_TOKEN)
    ffbot.add_handlers(HANDLERS)
    logger.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.run_polling()


if __name__ == '__main__':
    main()
