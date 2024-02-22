from telegram.ext import CommandHandler, BaseHandler, ConversationHandler

from bot.conversations.add_expense import get_expense_add_handler_params
from bot.conversations.add_income import get_income_add_handler_params
from bot.conversations.add_category import get_category_add_handler_params
from bot.handlers import rm_last_expense_handler, start_handler, help_handler, utc_offset_handler


HANDLERS: list[BaseHandler] = [
    CommandHandler('start', start_handler),                      # start
    CommandHandler('help', help_handler),                        # help
    CommandHandler('rm_last_expense', rm_last_expense_handler),  # rm_last_expense
    CommandHandler('utc_offset', utc_offset_handler),            # utc_offset
    ConversationHandler(**get_expense_add_handler_params()),     # add
    ConversationHandler(**get_income_add_handler_params()),      # boost_income
    ConversationHandler(**get_category_add_handler_params()),    # new_category
]
