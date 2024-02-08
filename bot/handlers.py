from telegram import Update
from telegram.ext import ContextTypes

from constants import START_MESSAGE, COMMANDS


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(START_MESSAGE)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_lines = [f'• /{command} — {description}' for command, description in COMMANDS.items()]
    await update.message.reply_text('Вам доступны следующие команды:')
    await update.message.reply_text('\n'.join(message_lines))
