from telegram.ext import CommandHandler, BaseHandler

from bot.handlers import start_handler, help_handler, category_add_handler


HANDLERS: list[BaseHandler] = [
    CommandHandler('start', start_handler),  # start
    CommandHandler('help', help_handler),  # help
    CommandHandler('new_category', category_add_handler),  # new_category
]
