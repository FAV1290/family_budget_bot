import logging
import datetime

from bot import FamilyFundsBot
from bot.routing import HANDLERS
from constants import LOGGING_FORMAT, API_TOKEN


logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, filename='bot.log')


def main() -> None:
    ffbot = FamilyFundsBot(API_TOKEN)
    ffbot.add_handlers(HANDLERS)
    logging.info(f'\n\n\n{datetime.datetime.now()}: Bot has started')
    ffbot.run_polling()


if __name__ == '__main__':
    main()




# from db.expenses import pop_last_user_expense
# from apps.categories import make_categories_report
# from apps.expenses import make_expenses_report
# from apps.incomes import make_incomes_report
# from bot.add_expense_dialog import add_expense_handler
# from bot.add_category_dialog import add_category_handler
# from bot.utc_offset_dialog import add_utc_offset_handler
# from bot.add_income_dialog import add_income_handler
# from bot.change_category_limit_dialog import change_category_limit_handler



'''
def show_expenses_handler(update, context):
    expenses_report = make_expenses_report(update.message.chat.id)
    update.message.reply_text(expenses_report, quote=False)
'''
'''
def show_categories_handler(update, context):
    categories_report = make_categories_report(update.message.chat.id)
    update.message.reply_text(categories_report, quote=False)
'''
'''
def show_incomes_handler(update, context):
    incomes_report = make_incomes_report(update.message.chat.id)
    update.message.reply_text(incomes_report, quote=False)
'''
'''
def pop_last_expense_handler(update, context):  #push logic to another module(s)?
    last_expense = pop_last_user_expense(update.message.chat.id)
    if last_expense.description is None:
        last_expense.description = '-'
    report_elements = [
        'Удален последний расход со следующими параметрами:',
        f'• Сумма расхода: {last_expense.amount}',
        f'• Категория: {last_expense.category}',
        f'• Описание: {last_expense.description}',
        f'• Дата и время создания: {last_expense.created_at.strftime("%d.%m.%Y, %H:%M:%S")}',
    ]
    update.message.reply_text('\n'.join(report_elements), quote=False)
'''
    # dp.add_handler(add_expense_handler()) #add
    # dp.add_handler(add_category_handler()) #new_category
    # dp.add_handler(add_utc_offset_handler()) #utc_offset
    # dp.add_handler(add_income_handler()) #boost_income
    # dp.add_handler(change_category_limit_handler()) #category_limit
    # dp.add_handler(CommandHandler('categories', show_categories_handler)) #categories
    # dp.add_handler(CommandHandler('expenses', show_expenses_handler)) #expenses
    # dp.add_handler(CommandHandler('incomes', show_incomes_handler)) #incomes
    # dp.add_handler(CommandHandler('rm_last_expense', pop_last_expense_handler)) #rm_last_expense
