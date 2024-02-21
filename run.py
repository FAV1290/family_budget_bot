import logging
import datetime

import alembic.command
import alembic.config

from bot import FamilyFundsBot
from bot.routing import HANDLERS
from constants import LOGGING_FORMAT, API_TOKEN, BOT_LOG_FILEPATH


def main() -> None:
    alembic_config = alembic.config.Config('alembic.ini')
    alembic.command.check(alembic_config)

    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, filename=BOT_LOG_FILEPATH)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)
    logger.info(f'{datetime.datetime.now()}: Bot is starting...')

    ffbot = FamilyFundsBot(API_TOKEN)
    ffbot.add_handlers(HANDLERS)
    ffbot.run_polling()


if __name__ == '__main__':
    main()
