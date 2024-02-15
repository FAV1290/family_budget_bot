from telegram.ext import CommandHandler, BaseHandler

from bot.handlers import start_handler, help_handler


HANDLERS: list[BaseHandler] = [
    CommandHandler('start', start_handler),  #start
    CommandHandler('help', help_handler),  #help
]
