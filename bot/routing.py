from telegram.ext import CommandHandler

from bot.handlers import start_handler, help_handler


HANDLERS = [
    CommandHandler('start', start_handler),  #start
    CommandHandler('help', help_handler),  #help
]
