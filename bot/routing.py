from telegram.ext import CommandHandler, BaseHandler

from bot.conversations.add_expense import add_expense_handler
from bot.handlers import (
    start_handler, help_handler, utc_offset_set_handler,
    category_add_handler, income_add_handler, expense_add_handler, rm_last_expense_handler
)


HANDLERS: list[BaseHandler] = [
    CommandHandler('start', start_handler),                      # start
    CommandHandler('help', help_handler),                        # help
    CommandHandler('new_category', category_add_handler),        # new_category
    CommandHandler('boost_income', income_add_handler),          # boost_income
    #CommandHandler('add', expense_add_handler),                  # add
    CommandHandler('rm_last_expense', rm_last_expense_handler),  # rm_last_expense
    CommandHandler('utc_offset', utc_offset_set_handler),        # utc_offset
    add_expense_handler,
]
