from telegram.ext import CommandHandler, BaseHandler, ConversationHandler

from bot.conversations.add_income import get_income_add_handler_params
from bot.conversations.add_expense import get_expense_add_handler_params
from bot.conversations.add_category import get_category_add_handler_params
from bot.conversations.update_utc_offset import get_update_utc_offset_handler_params
from bot.conversations.update_category_limit import get_update_category_limit_handler_params
from bot.handlers import (
    start_handler, help_handler, rm_last_expense_handler,
    incomes_report_handler, expenses_report_handler, categories_report_handler,
)


HANDLERS: list[BaseHandler] = [
    CommandHandler("start", start_handler),                             # (S)tart
    CommandHandler("help", help_handler),                               # (H)elp
    CommandHandler("rm_last_expense", rm_last_expense_handler),         # (R)m_last_expense
    CommandHandler("incomes", incomes_report_handler),                  # (I)ncomes
    CommandHandler("expenses", expenses_report_handler),                # (E)xpenses
    CommandHandler("categories", categories_report_handler),            # (C)ategories
    ConversationHandler(**get_update_category_limit_handler_params()),  # (L)imit_category
    ConversationHandler(**get_update_utc_offset_handler_params()),      # (U)tc_offset
    ConversationHandler(**get_expense_add_handler_params()),            # (A)dd
    ConversationHandler(**get_income_add_handler_params()),             # (B)oost_income
    ConversationHandler(**get_category_add_handler_params()),           # (N)ew_category
]
